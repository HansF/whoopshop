#!/usr/bin/env python3
"""Persistent Betaflight CLI session over USB serial.

A single `CliSession` owns the serial port for the whole exchange, so a
sequence of commands runs inside one CLI session instead of reopening the
port per command. Results are returned as data rather than printed, and CLI
exit discipline is enforced in a `finally` block so the Flight Controller is
never left locked in CLI mode -- even when the body raises.

Usage:
    from tools.fc_session import CliSession

    with CliSession() as fc:
        status = fc.run("status")
        values = fc.run_many(["get dshot_bidir", "get motor_poles"])

    # Applying changes: save=True writes EEPROM and reboots the FC.
    with CliSession(save=True) as fc:
        fc.run("set craft_name = WHOOP")
"""
import sys
import time

try:
    from tools.bf_cli import find_fc_port, read_until_prompt
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import find_fc_port, read_until_prompt


class CliError(RuntimeError):
    """Raised when the Flight Controller cannot enter or complete a CLI session."""


def _default_serial_factory(port, baud, timeout):
    import serial
    return serial.Serial(port, baud, timeout=timeout)


class CliSession:
    """Context manager holding one Betaflight CLI session open.

    Args:
        port: Serial device path. Auto-detected when omitted.
        save: End the session with `save` (writes EEPROM, reboots FC) instead
            of `exit noreboot`.
        serial_factory: Callable (port, baud, timeout) -> serial-like object.
            Injected by the test suite to run against `tools.fake_fc`.
    """

    def __init__(self, port=None, save=False, baud=115200, timeout=0.2,
                 serial_factory=None, verbose=True, delay_scale=1.0):
        self.port = port
        self.save = save
        self.baud = baud
        self.timeout = timeout
        self.verbose = verbose
        # Scales the settle delays below. The test suite drops this to ~0 so
        # the fake flight controller does not spend real seconds sleeping.
        self.delay_scale = delay_scale
        # How long the line must stay silent after a '#' before the reply is
        # considered complete. Real hardware needs the gap; the fake does not.
        self.quiet_for = 0.3 * delay_scale if delay_scale else 0.0
        # How long to wait for the '#' prompt before declaring the board stuck.
        self.handshake_timeout = 6.0 * delay_scale if delay_scale else 0.2
        self._serial_factory = serial_factory or _default_serial_factory
        self._ser = None
        self.sent = []          # every line written, for tests and auditing
        self.exited = False

    # -- lifecycle ---------------------------------------------------------

    def __enter__(self):
        if self.port is None:
            self.port = find_fc_port()

        self._log(f"# Connecting to Flight Controller on {self.port}...")

        try:
            self._ser = self._serial_factory(self.port, self.baud, self.timeout)
        except Exception as err:
            raise CliError(
                f"Failed to open port {self.port}: {err}\n"
                "Ensure no other program (Betaflight Configurator, a serial "
                "terminal) is holding the port."
            )

        try:
            self._handshake()
        except Exception:
            # Never leak an open port if the handshake fails.
            self._close()
            raise

        return self

    def __exit__(self, exc_type, exc, tb):
        # Exit discipline runs regardless of how the body ended. A failure to
        # write the exit command must not mask an in-flight exception.
        try:
            self._exit_cli()
        except Exception as err:
            if exc_type is None:
                raise
            self._log(f"# WARNING: could not send CLI exit command: {err}")
        finally:
            self._close()
        return False

    def _handshake(self):
        """Enter CLI mode with a bare '#' byte (no line terminator)."""
        self._ser.dtr = True
        time.sleep(0.4 * self.delay_scale)
        self._ser.reset_input_buffer()

        self._ser.write(b"#")
        self._ser.flush()

        prompt = read_until_prompt(self._ser, timeout=self.handshake_timeout,
                                   quiet_for=self.quiet_for)
        if "#" not in prompt:
            raise CliError(
                "No CLI prompt received from the Flight Controller.\n"
                "Possible causes:\n"
                "  1. FC stuck in CLI mode from an interrupted session -> replug USB.\n"
                "  2. FC is in DFU or Mass Storage mode -> replug USB.\n"
                "  3. Serial port speed mismatch."
            )

    def _exit_cli(self):
        if self.exited or self._ser is None:
            return
        cmd = "save" if self.save else "exit noreboot"
        self._write_line(cmd)
        time.sleep((1.5 if self.save else 0.5) * self.delay_scale)
        self.exited = True
        if self.save:
            self._log("# Saved settings to EEPROM. FC rebooting.")
        else:
            self._log("# Exited CLI mode cleanly (no reboot). FC ready for MSP.")

    def _close(self):
        if self._ser is not None:
            try:
                self._ser.close()
            except Exception:
                pass
            self._ser = None

    # -- commands ----------------------------------------------------------

    def run(self, command, timeout=60.0):
        """Send one command and return its output as text."""
        if self._ser is None:
            raise CliError("CLI session is not open. Use `with CliSession() as fc:`.")

        self._ser.reset_input_buffer()
        self._write_line(command)
        raw = read_until_prompt(self._ser, timeout=timeout, quiet_for=self.quiet_for)
        return self._clean(command, raw)

    def finish(self, command="save", settle=2.0):
        """Send a terminating command that reboots the board.

        `save`, `defaults` and `msc` drop the USB link, so no prompt comes
        back. This writes the command, waits for the reboot to begin, and
        marks the session closed so `__exit__` does not then try to send
        `exit noreboot` down a port that is going away.
        """
        if self._ser is None:
            raise CliError("CLI session is not open.")
        self._write_line(command)
        time.sleep(settle * self.delay_scale if self.delay_scale else 0)
        self.exited = True
        self._log(f"# Sent `{command}`; the FC is rebooting.")

    def run_many(self, commands, timeout=60.0):
        """Send several commands, returning an ordered {command: output} map."""
        results = {}
        for cmd in commands:
            results[cmd] = self.run(cmd, timeout=timeout)
        return results

    # -- internals ---------------------------------------------------------

    @staticmethod
    def _clean(command, raw):
        """Strip the echoed command and the trailing `#` prompt from a reply.

        Callers get the command's actual output and nothing else, which is what
        makes a captured `diff all` replayable as a restore.
        """
        text = raw.replace("\r\n", "\n").replace("\r", "\n")
        lines = text.split("\n")
        if lines and lines[0].strip() == command.strip():
            lines = lines[1:]
        while lines and lines[-1].strip() in ("#", ""):
            lines.pop()
        while lines and not lines[0].strip():
            lines.pop(0)
        return "\n".join(lines)

    def _write_line(self, command):
        self.sent.append(command)
        self._ser.write((command + "\r\n").encode("utf-8"))
        self._ser.flush()

    def _log(self, message):
        if self.verbose:
            print(message, file=sys.stderr)


def run_commands(commands, port=None, save=False, serial_factory=None,
                 verbose=True, delay_scale=1.0):
    """Convenience wrapper: open a session, run commands, return {cmd: output}."""
    with CliSession(port=port, save=save, serial_factory=serial_factory,
                    verbose=verbose, delay_scale=delay_scale) as fc:
        return fc.run_many(commands)
