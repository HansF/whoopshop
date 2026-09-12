"""Tests for the generated variable table and value validation.

The table in tools/bf_vars_table.py is read from a live flight controller by
tools/dump_vars.py, so these tests check its shape and the checking it enables,
not the specific values of any one board's settings.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.bf_vars import KNOWN_VARS, validate, value_problem
from tools.bf_vars_table import FIRMWARE, VARIABLES
from tools.dump_vars import firmware_line, parse_get_all

# Verbatim shape of a bare `get` reply, including a profile-scoped variable
# whose scope line sits between its value and its constraint.
SAMPLE_DUMP = """gyro_hardware_lpf = NORMAL
Allowed values: NORMAL, OPTION_1, OPTION_2, EXPERIMENTAL

dyn_idle_min_rpm = 0
profile 2
Allowed range: 0 - 200

craft_name = Crafty
String length: 1 - 16
Default value: -

acc_calibration = 0,0,0
Array length: 3

vtx_band = 5
Allowed range: 0 - 8
Default value: 0
"""


class TableShapeTest(unittest.TestCase):

    def test_table_is_populated(self):
        self.assertGreater(len(VARIABLES), 400)
        self.assertEqual(set(VARIABLES), set(KNOWN_VARS))

    def test_every_entry_declares_a_kind(self):
        kinds = {"enum", "int", "string", "array"}
        for name, entry in VARIABLES.items():
            self.assertIn(entry.get("kind"), kinds, name)

    def test_enums_carry_values_and_ints_carry_a_range(self):
        for name, entry in VARIABLES.items():
            if entry["kind"] == "enum":
                self.assertTrue(entry.get("values"), name)
            elif entry["kind"] == "int":
                self.assertIn("min", entry, name)
                self.assertLessEqual(entry["min"], entry["max"], name)

    def test_firmware_is_recorded(self):
        self.assertIn("Betaflight", FIRMWARE)

    def test_names_the_tools_use_are_present(self):
        for name in ("craft_name", "dyn_idle_min_rpm", "serialrx_provider",
                     "dshot_bidir", "motor_poles", "vtx_band", "blackbox_device"):
            self.assertIn(name, KNOWN_VARS)


class ParseDumpTest(unittest.TestCase):

    def setUp(self):
        self.parsed = parse_get_all(SAMPLE_DUMP)

    def test_finds_every_variable(self):
        self.assertEqual(set(self.parsed), {
            "gyro_hardware_lpf", "dyn_idle_min_rpm", "craft_name",
            "acc_calibration", "vtx_band",
        })

    def test_profile_scope_line_does_not_break_the_block(self):
        """The scope line sits between value and constraint and must be kept."""
        entry = self.parsed["dyn_idle_min_rpm"]
        self.assertEqual(entry["kind"], "int")
        self.assertEqual((entry["min"], entry["max"]), (0, 200))
        self.assertEqual(entry["scope"], "profile")

    def test_enum_values_are_captured(self):
        self.assertEqual(self.parsed["gyro_hardware_lpf"]["values"],
                         ["NORMAL", "OPTION_1", "OPTION_2", "EXPERIMENTAL"])

    def test_string_and_array_kinds(self):
        self.assertEqual(self.parsed["craft_name"]["kind"], "string")
        self.assertEqual(self.parsed["craft_name"]["maxlen"], 16)
        self.assertEqual(self.parsed["acc_calibration"]["kind"], "array")

    def test_firmware_line_extraction(self):
        self.assertTrue(firmware_line(
            "# Betaflight / STM32G47X (G473) 2026.6.0-alpha\n# board: x"
        ).startswith("Betaflight /"))


class ValueValidationTest(unittest.TestCase):

    def test_enum_value_outside_the_list_is_rejected(self):
        problem = value_problem("set serialrx_provider = CRSFF", "serialrx_provider")
        self.assertIn("not one of", problem)

    def test_enum_value_is_case_insensitive(self):
        self.assertIsNone(value_problem("set serialrx_provider = crsf",
                                        "serialrx_provider"))

    def test_integer_outside_its_range_is_rejected(self):
        problem = value_problem("set vtx_band = 99", "vtx_band")
        self.assertIn("outside the allowed range", problem)

    def test_integer_inside_its_range_passes(self):
        self.assertIsNone(value_problem("set vtx_band = 5", "vtx_band"))

    def test_overlong_string_is_rejected(self):
        problem = value_problem("set craft_name = " + "X" * 40, "craft_name")
        self.assertIn("character limit", problem)

    def test_fractional_values_are_not_misread_as_integers(self):
        """blackbox_sample_rate takes values like 1/4."""
        self.assertEqual(validate(["set blackbox_sample_rate = 1/4"]), [])

    def test_get_commands_are_not_value_checked(self):
        self.assertIsNone(value_problem("get vtx_band", "vtx_band"))

    def test_validate_surfaces_value_problems(self):
        problems = validate(["set vtx_band = 99", "set dyn_idle_min_rpm = 900"])
        self.assertEqual(len(problems), 2)


if __name__ == "__main__":
    unittest.main()
