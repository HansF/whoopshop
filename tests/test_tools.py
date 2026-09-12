"""Tests for the tools that talk to the flight controller through CliSession."""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import backup_restore, capture_log, motor_tool, preflight
from tools.bf_vars import validate
from tools.fake_fc import FakeFlightController
from tools.fc_session import CliSession

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def bound_session(fake):
    """A CliSession subclass wired to `fake`, for patching into a tool."""
    class BoundSession(CliSession):
        def __init__(self, *args, **kwargs):
            kwargs.update(serial_factory=fake.as_factory(),
                          delay_scale=0, verbose=False)
            kwargs.setdefault("port", "FAKE")
            super().__init__(*args, **kwargs)
    return BoundSession


class MotorSafetyTest(unittest.TestCase):
    """A motor left spinning on the bench is the worst failure here."""

    def test_refuses_without_props_off(self):
        with self.assertRaises(SystemExit):
            motor_tool.test_motor_spin(1, props_off=False)

    def test_refuses_unsafe_throttle(self):
        with self.assertRaises(SystemExit):
            motor_tool.test_motor_spin(1, props_off=True, throttle=1800)

    def test_stops_motor_after_normal_spin(self):
        fake = FakeFlightController()
        with mock.patch.object(motor_tool, "CliSession", bound_session(fake)):
            motor_tool.test_motor_spin(1, props_off=True, duration=0)
        self.assertIn("motor 1 1050", fake.commands)
        self.assertIn("motor 1 1000", fake.commands)
        self.assertLess(fake.commands.index("motor 1 1050"),
                        fake.commands.index("motor 1 1000"))

    def test_stops_motor_when_spin_raises(self):
        """A dropped link mid-spin must still send the stop command."""
        fake = FakeFlightController(
            raise_on={"motor 1 1050": RuntimeError("cable yanked")})
        with mock.patch.object(motor_tool, "CliSession", bound_session(fake)):
            with self.assertRaises(RuntimeError):
                motor_tool.test_motor_spin(1, props_off=True, duration=0)
        self.assertIn("motor 1 1000", fake.commands)

    def test_stops_motor_on_keyboard_interrupt(self):
        """Ctrl-C during a spin must not leave the motor running."""
        fake = FakeFlightController(raise_on={"motor 1 1050": KeyboardInterrupt()})
        with mock.patch.object(motor_tool, "CliSession", bound_session(fake)):
            with self.assertRaises(KeyboardInterrupt):
                motor_tool.test_motor_spin(1, props_off=True, duration=0)
        self.assertIn("motor 1 1000", fake.commands)
        self.assertEqual(fake.commands[-1], "exit noreboot")


class BackupTest(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(FIXTURES, "diff_all.txt"), encoding="utf-8") as handle:
            self.diff = handle.read()

    def test_extract_drops_comments_and_blanks(self):
        commands = backup_restore.extract_commands(self.diff)
        self.assertTrue(commands)
        for command in commands:
            self.assertFalse(command.startswith("#"))
            self.assertEqual(command, command.strip())
            self.assertTrue(command)

    def test_extract_keeps_real_commands(self):
        commands = backup_restore.extract_commands(self.diff)
        for expected in ("batch start", "batch end", "board_name BETAFPVG473",
                         "set craft_name = WHOOP", "profile 0"):
            self.assertIn(expected, commands)

    def test_no_banner_text_survives_capture(self):
        """The old stdout-scraping capture embedded '===== diff all ====='."""
        fake = FakeFlightController()
        with bound_session(fake)() as fc:
            captured = fc.run("diff all")
        commands = backup_restore.extract_commands(captured)
        self.assertNotIn("=====", " ".join(commands))
        for command in commands:
            self.assertFalse(command.startswith("====="))

    def test_roundtrip_is_lossless(self):
        """Capture, write, read back: the command list must be identical."""
        fake = FakeFlightController()
        with bound_session(fake)() as fc:
            captured = fc.run("diff all")
        original = backup_restore.extract_commands(captured)

        file_text = (
            "# WhoopShop FC backup created 2026-09-12_100000\n"
            "# Port: FAKE\n#\n" + captured + "\n"
        )
        self.assertEqual(backup_restore.extract_commands(file_text), original)

    def test_restore_resets_to_defaults_first(self):
        fake = FakeFlightController()
        with mock.patch.object(backup_restore, "CliSession", bound_session(fake)):
            path = os.path.join(FIXTURES, "diff_all.txt")
            backup_restore.restore_backup(path, assume_yes=True)
        self.assertEqual(fake.commands[0], "defaults nosave")
        self.assertEqual(fake.commands[-1], "save")
        self.assertIn("set craft_name = WHOOP", fake.commands)

    def test_restore_aborts_without_confirmation(self):
        fake = FakeFlightController()
        with mock.patch.object(backup_restore, "CliSession", bound_session(fake)), \
             mock.patch("builtins.input", return_value="no"):
            with self.assertRaises(SystemExit):
                backup_restore.restore_backup(os.path.join(FIXTURES, "diff_all.txt"))
        self.assertEqual(fake.commands, [])


class CaptureLogTest(unittest.TestCase):
    """`status` carries no board name, so `version` has to be read as well."""

    def test_board_name_comes_from_version(self):
        info = capture_log.parse_version(
            "# Betaflight / STM32F7X2 (S7X2) 4.5.1 Jun  1 2026 / 10:00:00 MSP API: 1.46\n"
            "# board: manufacturer_id: BEFH, board_name: BETAFPVG473\n")
        self.assertEqual(info["board"], "BETAFPVG473")
        self.assertTrue(info["firmware"].startswith("Betaflight /"))

    def test_version_without_board_line_is_tolerated(self):
        self.assertNotIn("board", capture_log.parse_version("# Betaflight / F405 4.4.0"))

    def test_craft_name_survives_a_colliding_variable(self):
        """`get craft_name` also returns `osd_craft_name_pos`, listed first."""
        fake = FakeFlightController()
        with mock.patch.object(capture_log, "CliSession", bound_session(fake)):
            metrics = capture_log.capture_telemetry()
        self.assertEqual(metrics["craft_name"], "WHOOP")
        self.assertNotEqual(metrics["craft_name"], "395")

    def test_telemetry_fills_board_and_craft_name(self):
        fake = FakeFlightController()
        with mock.patch.object(capture_log, "CliSession", bound_session(fake)):
            metrics = capture_log.capture_telemetry()
        self.assertEqual(metrics["board"], "BETAFPVG473")
        self.assertEqual(metrics["craft_name"], "WHOOP")
        self.assertEqual(fake.commands[-1], "exit noreboot")

    def test_craft_name_ignores_allowed_values_line(self):
        """A reply's second line must not leak into the value."""
        fake = FakeFlightController(
            responses={"get craft_name": "craft_name = WHOOP\nAllowed values: 1-16"})
        with mock.patch.object(capture_log, "CliSession", bound_session(fake)):
            metrics = capture_log.capture_telemetry()
        self.assertEqual(metrics["craft_name"], "WHOOP")

    def test_telemetry_failure_degrades_gracefully(self):
        fake = FakeFlightController(prompt_on_handshake=False)
        with mock.patch.object(capture_log, "CliSession", bound_session(fake)):
            metrics = capture_log.capture_telemetry()
        self.assertEqual(metrics["board"], "Unknown")


class SelfContainedRestoreTest(unittest.TestCase):
    """Real firmware emits a diff that is already a complete restore script.

    It opens with `batch start`, resets with `defaults nosave`, and closes with
    `save`. Re-wrapping such a file resets twice and sends a second `save` to a
    board the first one already rebooted.
    """

    PATH = os.path.join(FIXTURES, "diff_self_contained.txt")

    def test_fixture_matches_real_firmware_shape(self):
        commands = backup_restore.extract_commands(open(self.PATH).read())
        self.assertEqual(commands[0], "batch start")
        self.assertIn("defaults nosave", commands)
        self.assertEqual(commands[-1], "save")

    def test_defaults_is_not_sent_twice(self):
        fake = FakeFlightController()
        with mock.patch.object(backup_restore, "CliSession", bound_session(fake)):
            backup_restore.restore_backup(self.PATH, assume_yes=True)
        self.assertEqual(fake.commands.count("defaults nosave"), 1)

    def test_save_is_not_sent_twice(self):
        fake = FakeFlightController()
        with mock.patch.object(backup_restore, "CliSession", bound_session(fake)):
            backup_restore.restore_backup(self.PATH, assume_yes=True)
        self.assertEqual(fake.commands.count("save"), 1)
        self.assertEqual(fake.commands[-1], "save")

    def test_no_exit_command_follows_the_reboot(self):
        fake = FakeFlightController()
        with mock.patch.object(backup_restore, "CliSession", bound_session(fake)):
            backup_restore.restore_backup(self.PATH, assume_yes=True)
        self.assertNotIn("exit noreboot", fake.commands)

    def test_plain_command_list_still_gets_wrapped(self):
        """A file without the scaffolding must still be reset and saved."""
        fake = FakeFlightController()
        with mock.patch.object(backup_restore, "CliSession", bound_session(fake)):
            backup_restore.restore_backup(
                os.path.join(FIXTURES, "diff_all.txt"), assume_yes=True)
        self.assertEqual(fake.commands[0], "defaults nosave")
        self.assertEqual(fake.commands[-1], "save")


class FlashWarningTest(unittest.TestCase):

    def test_full_flash_warns_rather_than_informs(self):
        rows = preflight.parse_audit_results(
            {"flash_info": "FlashFS size=16777216, usedSize=16777216"})
        item, status, detail = rows[0]
        self.assertEqual(status, "WARN")
        self.assertIn("FULL", detail)

    def test_mostly_empty_flash_passes(self):
        rows = preflight.parse_audit_results(
            {"flash_info": "FlashFS size=16777216, usedSize=2097152"})
        self.assertEqual(rows[0][1], "PASS")

    def test_unparseable_flash_line_falls_back_to_info(self):
        rows = preflight.parse_audit_results({"flash_info": "usedSize unknown"})
        self.assertEqual(rows[0][1], "INFO")


class PreflightTest(unittest.TestCase):

    def test_audit_commands_are_valid(self):
        self.assertEqual(validate(preflight.AUDIT_COMMANDS), [])

    def test_report_flags_blocking_arming_reason(self):
        rows = preflight.parse_audit_results(
            {"status": "Arming disable flags: CLI MSP THROTTLE"})
        statuses = {item: status for item, status, _ in rows}
        self.assertEqual(statuses["Arming Disable Flags"], "WARN")

    def test_cli_and_msp_alone_are_not_a_warning(self):
        rows = preflight.parse_audit_results(
            {"status": "Arming disable flags: CLI MSP"})
        statuses = {item: status for item, status, _ in rows}
        self.assertEqual(statuses["Arming Disable Flags"], "PASS")

    def test_bidirectional_dshot_off_warns(self):
        rows = preflight.parse_audit_results({"get dshot_bidir": "dshot_bidir = OFF"})
        statuses = {item: status for item, status, _ in rows}
        self.assertEqual(statuses["Bi-directional DShot"], "WARN")

    def test_receiver_provider_ignores_colliding_variables(self):
        reply = ("osd_rx_provider_pos = 2048\n\n"
                 "serialrx_provider = CRSF\nDefault value: 0")
        rows = preflight.parse_audit_results({"get serialrx_provider": reply})
        details = {item: detail for item, _, detail in rows}
        self.assertEqual(details["Receiver Provider"], "CRSF")


if __name__ == "__main__":
    unittest.main()
