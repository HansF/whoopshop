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
    parse_get,
    validate,
    variable_name,
)

# Verbatim from a BETAFPVG473_V2 running firmware 2026.6.0-alpha. Betaflight's
# `get` matches on substring, and lists the partial match first.
REAL_CRAFT_NAME_REPLY = """osd_craft_name_pos = 395
Allowed range: 0 - 65535
Default value: 341

craft_name = Crafty
String length: 1 - 16
Default value: -"""


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


class ParseGetTest(unittest.TestCase):
    """`get` returns every variable containing the query, partial match first."""

    def test_exact_name_wins_over_earlier_partial_match(self):
        self.assertEqual(parse_get(REAL_CRAFT_NAME_REPLY, "craft_name"), "Crafty")

    def test_naive_first_match_would_have_been_wrong(self):
        """Documents the bug: the first '=' line belongs to another variable."""
        naive = REAL_CRAFT_NAME_REPLY.split("=", 1)[1].splitlines()[0].strip()
        self.assertEqual(naive, "395")
        self.assertNotEqual(naive, parse_get(REAL_CRAFT_NAME_REPLY, "craft_name"))

    def test_the_partial_match_is_still_readable_by_its_own_name(self):
        self.assertEqual(parse_get(REAL_CRAFT_NAME_REPLY, "osd_craft_name_pos"), "395")

    def test_simple_reply(self):
        self.assertEqual(parse_get("dshot_bidir = ON", "dshot_bidir"), "ON")

    def test_absent_name_returns_none(self):
        self.assertIsNone(parse_get("dshot_bidir = ON", "motor_poles"))

    def test_metadata_lines_are_ignored(self):
        reply = "vtx_band = 5\nAllowed range: 0 - 8\nDefault value: 0"
        self.assertEqual(parse_get(reply, "vtx_band"), "5")


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
