"""Tests for the Blackbox analyzer.

The fixture `decoded_log.csv` is synthetic with known properties:
  * motors 1-3 hold 3000 eRPM at output 1500; motor 4 holds 2700 (10% down)
  * roll carries a 200 Hz tone at amplitude 10 and a 600 Hz tone at amplitude 2
  * logged at 8 kHz
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tools.analyze_log as analyze_log
from tools.analyze_log import (
    analyze,
    format_markdown,
    gyro_noise_floor,
    load_csv,
    motor_balance,
    sample_rate_hz,
)

FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "fixtures", "decoded_log.csv")


class LoadTest(unittest.TestCase):

    def test_columns_are_stripped_and_numeric(self):
        columns = load_csv(FIXTURE)
        self.assertIn("gyroADC[0]", columns)
        self.assertIn("motor[0]", columns)
        self.assertIsInstance(columns["motor[0]"][0], float)

    def test_sample_rate_from_time_column(self):
        self.assertAlmostEqual(sample_rate_hz(load_csv(FIXTURE)), 8000.0, places=1)

    def test_sample_rate_falls_back_without_time(self):
        self.assertEqual(sample_rate_hz({"gyroADC[0]": [1.0, 2.0]}), 8000.0)


class MotorBalanceTest(unittest.TestCase):

    def setUp(self):
        self.rows = motor_balance(load_csv(FIXTURE))

    def test_ratio_is_erpm_over_output(self):
        self.assertAlmostEqual(self.rows[0]["ratio"], 3000.0 / 1500.0, places=6)

    def test_degraded_motor_is_flagged_by_deviation(self):
        deviations = [row["deviation_pct"] for row in self.rows]
        self.assertAlmostEqual(deviations[3], -7.6923, places=3)
        for healthy in deviations[:3]:
            self.assertAlmostEqual(healthy, 2.5641, places=3)

    def test_missing_erpm_yields_none_not_zero(self):
        """Without bidirectional DShot there is no eRPM; say so, do not print 0.00."""
        rows = motor_balance({"motor[0]": [1500.0] * 10})
        self.assertIsNone(rows[0]["ratio"])
        self.assertIn("no eRPM data", format_markdown({
            "motors": rows, "gyro_noise": {}, "sample_rate_hz": 8000.0,
        }))


class FftTest(unittest.TestCase):

    @staticmethod
    def _tone(freq, amplitude=10.0, n=4096, rate=8000.0):
        return [amplitude * math.sin(2 * math.pi * freq * (i / rate)) for i in range(n)]

    def test_recovers_on_bin_tone_amplitude(self):
        """A Hann window halves a tone's amplitude; on-bin there is no loss."""
        rate, n = 8000.0, 4096
        freq = 102 * rate / n
        magnitudes = analyze_log._magnitudes(self._tone(freq, 10.0, n, rate))
        peak = max(range(len(magnitudes)), key=lambda i: magnitudes[i])
        self.assertEqual(peak, 102)
        self.assertAlmostEqual(magnitudes[peak], 5.0, places=2)

    def test_pure_python_matches_numpy(self):
        """The fallback FFT must agree with numpy to floating point precision."""
        if analyze_log._np is None:
            self.skipTest("numpy not installed; only one backend available")

        signal = self._tone(199.21875)
        with_numpy = analyze_log._magnitudes(signal)

        saved = analyze_log._np
        analyze_log._np = None
        try:
            without_numpy = analyze_log._magnitudes(signal)
        finally:
            analyze_log._np = saved

        self.assertEqual(len(with_numpy), len(without_numpy))
        worst = max(abs(a - b) for a, b in zip(with_numpy, without_numpy))
        self.assertLess(worst, 1e-9)

    def test_rejects_non_power_of_two(self):
        with self.assertRaises(ValueError):
            analyze_log._fft([1.0] * 100)


class GyroNoiseTest(unittest.TestCase):

    def test_broadband_noise_gives_nonzero_floor(self):
        import random
        random.seed(7)
        columns = {"gyroADC[0]": [random.gauss(0, 1.0) for _ in range(4096)]}
        floor = gyro_noise_floor(columns, 8000.0)
        self.assertGreater(floor["roll"], 0.005)

    def test_quiet_axis_has_lower_floor_than_noisy_axis(self):
        import random
        random.seed(11)
        columns = {
            "gyroADC[0]": [random.gauss(0, 5.0) for _ in range(4096)],
            "gyroADC[1]": [random.gauss(0, 0.5) for _ in range(4096)],
        }
        floor = gyro_noise_floor(columns, 8000.0)
        self.assertGreater(floor["roll"], floor["pitch"])

    def test_short_log_is_skipped_not_crashed(self):
        self.assertEqual(gyro_noise_floor({"gyroADC[0]": [1.0] * 10}, 8000.0), {})

    def test_missing_gyro_columns_yield_empty(self):
        self.assertEqual(gyro_noise_floor({"motor[0]": [1500.0] * 4096}, 8000.0), {})


class ReportTest(unittest.TestCase):

    def test_markdown_warns_about_the_degraded_motor(self):
        markdown = format_markdown(analyze(FIXTURE))
        self.assertIn("Motor 4", markdown)
        self.assertIn("Inspect bearings", markdown)

    def test_motor_ratios_are_computed_not_placeholders(self):
        """The old template hardcoded `0.00` for every motor."""
        markdown = format_markdown(analyze(FIXTURE))
        ratio_lines = [l for l in markdown.splitlines() if l.strip().startswith("- Motor")]
        self.assertEqual(len(ratio_lines), 4)
        for line in ratio_lines:
            self.assertNotIn("`0.00`", line)

    def test_small_noise_values_keep_significant_digits(self):
        """A quiet axis must not render as `0.00`, which reads as no data."""
        markdown = format_markdown({
            "motors": [], "sample_rate_hz": 8000.0,
            "gyro_noise": {"roll": 0.0012, "pitch": 3.5},
        })
        self.assertIn("`0.0012`", markdown)
        self.assertIn("`3.50`", markdown)


if __name__ == "__main__":
    unittest.main()
