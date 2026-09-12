#!/usr/bin/env python3
"""In-memory stand-in for a Betaflight flight controller over serial.

Lets the whole toolchain run, and be tested, with no drone plugged in. It is
duck-typed against the subset of `serial.Serial` that `tools/bf_cli.py` and
`tools/fc_session.py` actually use: `read`, `write`, `flush`, `dtr`,
`reset_input_buffer` and `close`.

Usage:
    from tools.fake_fc import FakeFlightController
    from tools.fc_session import CliSession

    fake = FakeFlightController()
    with CliSession(port="FAKE", serial_factory=fake.as_factory(),
                    delay_scale=0) as fc:
        print(fc.run("status"))

    assert fake.commands[-1] == "exit noreboot"

Responses come from `tests/fixtures/` by default. Pass `responses=` to
override a command, or `error_on=` to make specific commands fail the way the
firmware does.
"""
import os

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "fixtures"
)

PROMPT = b"\r\n# "


def _fixture(name):
    path = os.path.join(FIXTURE_DIR, name)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except FileNotFoundError:
        return ""


def default_responses():
    """Canned replies keyed by the exact command text."""
    return {
        "status": _fixture("status.txt"),
        "diff all": _fixture("diff_all.txt"),
        "diff": _fixture("diff_all.txt"),
        "get dshot_bidir": _fixture("get_dshot_bidir.txt"),
        "flash_info": (
            "Flash sectors=512, sectorSize=4096, pagesPerSector=16, "
            "pageSize=256, totalSize=2097152\n"
            "FlashFS: offset = 131072, usedSize = 131072"
        ),
        "save": "Saving...",
        "exit noreboot": "",
        "defaults nosave": "Resetting to defaults",
    }


class FakeFlightController:
    """A scriptable fake serial device speaking the Betaflight CLI.

    Attributes:
        commands: Every command line received, in order. Includes the closing
            `exit noreboot` or `save`, so exit discipline can be asserted.
        written: Raw byte payloads received, including the bare `#` handshake.
    """

    def __init__(self, responses=None, error_on=(), raise_on=None,
                 prompt_on_handshake=True):
        self.responses = default_responses()
        if responses:
            self.responses.update(responses)
        self.error_on = set(error_on)
        # {command: exception} -- simulates the link dying mid-command, e.g. a
        # yanked USB cable or a Ctrl-C. The command is recorded before the
        # exception fires, so cleanup behaviour stays observable.
        self.raise_on = dict(raise_on or {})
        self.prompt_on_handshake = prompt_on_handshake

        self.commands = []
        self.written = []
        self.closed = False
        self.dtr = False
        self._out = bytearray()

    # -- factory ----------------------------------------------------------

    def as_factory(self):
        """Return a (port, baud, timeout) -> self callable for CliSession."""
        def factory(port, baud, timeout):
            self.port = port
            self.baud = baud
            self.timeout = timeout
            return self
        return factory

    # -- serial.Serial surface --------------------------------------------

    def write(self, data):
        self.written.append(bytes(data))

        if data == b"#":
            # Bare '#' handshake: the board answers with a prompt only.
            if self.prompt_on_handshake:
                self._out += PROMPT
            return len(data)

        text = data.decode("utf-8", "replace").strip()
        if text:
            self.commands.append(text)
            if text in self.raise_on:
                raise self.raise_on[text]
            body = self._reply_for(text)
            echoed = text.encode("utf-8") + b"\r\n"
            self._out += echoed + body.encode("utf-8") + PROMPT
        return len(data)

    def read(self, size=1):
        if not self._out:
            return b""
        chunk = bytes(self._out[:size])
        del self._out[:size]
        return chunk

    def flush(self):
        pass

    def reset_input_buffer(self):
        self._out.clear()

    def reset_output_buffer(self):
        pass

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
        return False

    # -- behaviour --------------------------------------------------------

    def _reply_for(self, command):
        if command in self.error_on:
            return "Invalid name"
        if command in self.responses:
            return self.responses[command]

        head = command.split(None, 1)[0].lower()
        if head == "get":
            name = command.split(None, 1)[1].strip()
            return f"{name} = ON\nAllowed values: OFF, ON"
        if head == "set":
            remainder = command.split(None, 1)[1]
            name, _, value = remainder.partition("=")
            return f"{name.strip()} set to {value.strip()}"
        if head in ("motor", "map", "feature", "batch", "profile"):
            return ""
        return ""
