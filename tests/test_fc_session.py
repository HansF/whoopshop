"""Tests for the persistent CLI session and its exit discipline."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.fake_fc import FakeFlightController
from tools.fc_session import CliSession, CliError, run_commands


def session(fake, **kwargs):
    kwargs.setdefault("port", "FAKE")
    kwargs.setdefault("delay_scale", 0)
    kwargs.setdefault("verbose", False)
    return CliSession(serial_factory=fake.as_factory(), **kwargs)


class ExitDisciplineTest(unittest.TestCase):
    """CLAUDE.md makes clean CLI exit mandatory: a missed exit locks the FC."""

    def test_exits_cli_on_success(self):
        fake = FakeFlightController()
        with session(fake) as fc:
            fc.run("status")
        self.assertEqual(fake.commands[-1], "exit noreboot")
        self.assertTrue(fake.closed)

    def test_exits_cli_when_body_raises(self):
        fake = FakeFlightController()
        with self.assertRaises(ValueError):
            with session(fake) as fc:
                fc.run("status")
                raise ValueError("boom")
        self.assertEqual(fake.commands[-1], "exit noreboot")
        self.assertTrue(fake.closed)

    def test_save_replaces_exit(self):
        fake = FakeFlightController()
        with session(fake, save=True) as fc:
            fc.run("set craft_name = WHOOP")
        self.assertEqual(fake.commands[-1], "save")
        self.assertNotIn("exit noreboot", fake.commands)

    def test_port_closed_when_handshake_fails(self):
        fake = FakeFlightController(prompt_on_handshake=False)
        with self.assertRaises(CliError):
            with session(fake):
                pass
        self.assertTrue(fake.closed)


class OutputTest(unittest.TestCase):

    def test_handshake_sends_bare_hash(self):
        fake = FakeFlightController()
        with session(fake):
            pass
        self.assertEqual(fake.written[0], b"#")

    def test_run_returns_output_not_none(self):
        fake = FakeFlightController()
        with session(fake) as fc:
            out = fc.run("status")
        self.assertIn("Arming disable flags:", out)

    def test_output_excludes_echo_and_prompt(self):
        """The stdout-scraping era left banners in captured text. It must not."""
        fake = FakeFlightController()
        with session(fake) as fc:
            out = fc.run("diff all")
        self.assertFalse(out.startswith("diff all"))
        self.assertFalse(out.rstrip().endswith("#"))
        self.assertNotIn("=====", out)

    def test_run_many_maps_command_to_its_own_output(self):
        fake = FakeFlightController()
        with session(fake) as fc:
            results = fc.run_many(["get dshot_bidir", "get motor_poles"])
        self.assertEqual(list(results), ["get dshot_bidir", "get motor_poles"])
        self.assertIn("dshot_bidir", results["get dshot_bidir"])
        self.assertIn("motor_poles", results["get motor_poles"])

    def test_one_session_for_many_commands(self):
        """Commands must share a session rather than reopening the port."""
        fake = FakeFlightController()
        with session(fake) as fc:
            fc.run_many(["status", "get dshot_bidir", "flash_info"])
        self.assertEqual(fake.written.count(b"#"), 1)
        self.assertEqual(fake.commands.count("exit noreboot"), 1)

    def test_run_outside_session_is_refused(self):
        fake = FakeFlightController()
        fc = CliSession(port="FAKE", serial_factory=fake.as_factory(),
                        delay_scale=0, verbose=False)
        with self.assertRaises(CliError):
            fc.run("status")

    def test_run_commands_helper(self):
        fake = FakeFlightController()
        results = run_commands(["status"], port="FAKE",
                               serial_factory=fake.as_factory(),
                               delay_scale=0, verbose=False)
        self.assertIn("status", results)
        self.assertEqual(fake.commands[-1], "exit noreboot")


if __name__ == "__main__":
    unittest.main()
