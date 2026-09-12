"""Tests for the MSP v1 request/response implementation.

MSP is how live telemetry and RC channel values are read without putting the
board into CLI mode. It is a separate protocol from the CLI, with its own
binary framing and checksum, and had no coverage at all.
"""
import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.bf_msp import msp_request
from tools.fake_fc import FakeMspDevice

MSP_RC = 105
MSP_STATUS = 101


class MspRequestTest(unittest.TestCase):

    def test_request_frame_is_well_formed(self):
        """A request is $M< + length 0 + code + checksum (0 XOR code)."""
        device = FakeMspDevice({MSP_RC: b""})
        msp_request(device, MSP_RC)
        self.assertEqual(device.requested, [MSP_RC])

    def test_round_trips_rc_channel_payload(self):
        channels = [1500, 1500, 1000, 1500, 1000, 2000, 1000, 1000]
        payload = struct.pack("<" + "H" * len(channels), *channels)
        device = FakeMspDevice({MSP_RC: payload})

        received, error = msp_request(device, MSP_RC)

        self.assertIsNone(error)
        decoded = struct.unpack("<" + "H" * (len(received) // 2), received)
        self.assertEqual(list(decoded), channels)

    def test_empty_payload_is_not_an_error(self):
        received, error = msp_request(FakeMspDevice({MSP_STATUS: b""}), MSP_STATUS)
        self.assertIsNone(error)
        self.assertEqual(received, b"")

    def test_bad_checksum_is_rejected(self):
        device = FakeMspDevice({MSP_RC: b"\x01\x02\x03\x04"}, corrupt_checksum=True)
        received, error = msp_request(device, MSP_RC)
        self.assertIsNone(received)
        self.assertIn("Checksum", error)

    def test_error_frame_is_reported(self):
        device = FakeMspDevice({MSP_RC: b""}, send_error=True)
        received, error = msp_request(device, MSP_RC)
        self.assertIsNone(received)
        self.assertIn("rejected", error)

    def test_silence_times_out_rather_than_hanging(self):
        class Silent(FakeMspDevice):
            def write(self, data):
                return len(data)

        received, error = msp_request(Silent(), MSP_RC, timeout=0.05)
        self.assertIsNone(received)
        self.assertIn("Timeout", error)

    def test_checksum_covers_length_code_and_payload(self):
        """Recompute the reference checksum independently of the implementation."""
        payload = bytes([0x10, 0x20, 0x30])
        frame = FakeMspDevice.frame(MSP_RC, payload)
        expected = len(payload) ^ MSP_RC
        for byte in payload:
            expected ^= byte
        self.assertEqual(frame[-1], expected)
        self.assertEqual(frame[:3], b"$M>")


if __name__ == "__main__":
    unittest.main()
