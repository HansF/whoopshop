"""Tests for the Betaflight variable registry.

The names checked here are the ones that were shipped in this repo and would
be silently rejected by the firmware.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.bf_vars import (
    CliResponseError,
    UnknownVariableError,
    assert_valid,
    check_response,
    check_responses,
    validate,
    variable_name,
)


class VariableNameTest(unittest.TestCase):

    def test_extracts_name_from_set(self):
        self.assertEqual(variable_name("set dyn_idle_min_rpm = 30"), "dyn_idle_min_rpm")

    def test_extracts_name_from_get(self):
        self.assertEqual(variable_name("get dshot_bidir"), "dshot_bidir")

    def test_bare_commands_have_no_variable(self):
        for cmd in ("status", "diff all", "map AETR1234", "motor 1 1050"):
            self.assertIsNone(variable_name(cmd), cmd)


class ValidateTest(unittest.TestCase):

    def test_accepts_correct_commands(self):
        self.assertEqual(validate([
            "set dyn_idle_min_rpm = 30",
            "set anti_gravity_gain = 80",
            "set p_pitch = 52",
            "get dshot_bidir",
            "get serialrx_provider",
            "status",
            "map AETR1234",
            "flash_info",
        ]), [])

    def test_rejects_renamed_idle_variable(self):
        problems = validate(["set dynamic_idle_min_rpm = 30"])
        self.assertEqual(len(problems), 1)
        self.assertIn("dyn_idle_min_rpm", problems[0])

    def test_rejects_variables_that_are_really_commands(self):
        for cmd in ("get map", "set map = AETR11"):
            problems = validate([cmd])
            self.assertEqual(len(problems), 1, cmd)
            self.assertIn("bare", problems[0].lower() + problems[0])

    def test_rejects_invented_receiver_variables(self):
        problems = validate([
            "get rx_serial_protocol",
            "get crsf_use_painless_telemetry",
            "get telemetry_disabled",
        ])
        self.assertEqual(len(problems), 3)

    def test_rejects_unknown_variable(self):
        problems = validate(["set not_a_real_setting = 5"])
        self.assertEqual(len(problems), 1)
        self.assertIn("unknown variable", problems[0])

    def test_assert_valid_raises_with_all_problems(self):
        with self.assertRaises(UnknownVariableError) as ctx:
            assert_valid(["set dynamic_idle_min_rpm = 30", "get rx_serial_protocol"])
        message = str(ctx.exception)
        self.assertIn("dyn_idle_min_rpm", message)
        self.assertIn("serialrx_provider", message)

    def test_assert_valid_passes_clean_commands(self):
        assert_valid(["set dyn_idle_min_rpm = 30", "status"])


class ResponseTest(unittest.TestCase):

    def test_invalid_name_reply_raises(self):
        with self.assertRaises(CliResponseError):
            check_response("get nonsense", "nonsense\r\nInvalid name\r\n")

    def test_unknown_command_reply_raises(self):
        with self.assertRaises(CliResponseError):
            check_response("bogus", "Unknown command")

    def test_good_reply_passes(self):
        check_response("get dshot_bidir", "dshot_bidir = ON\nAllowed values: OFF, ON")

    def test_check_responses_scans_the_whole_map(self):
        with self.assertRaises(CliResponseError):
            check_responses({
                "get dshot_bidir": "dshot_bidir = ON",
                "get bogus": "Invalid name",
            })


if __name__ == "__main__":
    unittest.main()
