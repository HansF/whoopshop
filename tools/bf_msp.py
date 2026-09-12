#!/usr/bin/env python3
"""Read live Flight Controller status and RC channel values over MSP v1 (MultiWii Serial Protocol).

The FC must NOT be in CLI mode — CLI mode does not respond to MSP binary messages.
If unsure, run `python tools/bf_cli.py "status"` first to exit CLI mode cleanly.

Usage:
    python tools/bf_msp.py
    python tools/bf_msp.py --samples 10
    python tools/bf_msp.py --port COM3
"""
import argparse
import struct
import sys
import time

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: 'pyserial' package is not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


MSP_API_VERSION = 1
MSP_FC_VARIANT = 2
MSP_FC_VERSION = 3
MSP_STATUS = 101
MSP_RC = 105


def find_fc_port(target_port=None, target_serial=None):
    """Locate Flight Controller port across Windows, macOS, and Linux."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        raise SystemExit("No serial ports found. Is the Flight Controller plugged in?")

    if target_port:
        return target_port

    if target_serial:
        for p in ports:
            if p.serial_number == target_serial:
                return p.device
        raise SystemExit(f"Flight controller with serial number '{target_serial}' not found.")

    for p in ports:
        desc = p.description or ""
        dev = p.device
        if "radio" in desc.lower() or "edgetx" in desc.lower():
            continue
        if p.vid == 0x0483 and p.pid == 0x5740:
            return dev
        if "ACM" in dev or "usbmodem" in dev or "USB Serial" in desc:
            return dev

    return ports[0].device


def msp_request(ser, code, timeout=2.0):
    """Send MSP v1 request header ($M< + len + code + crc) and receive response ($M>)."""
    ser.reset_input_buffer()
    header = b"$M<" + bytes([0, code, 0 ^ code])
    ser.write(header)
    ser.flush()

    deadline = time.time() + timeout
    buf = b""

    while time.time() < deadline:
        chunk = ser.read(256)
        if chunk:
            buf += chunk
        else:
            time.sleep(0.01)

        idx = buf.find(b"$M")
        if idx < 0 or len(buf) < idx + 5:
            continue

        direction = buf[idx + 2:idx + 3]
        if direction == b"!":
            return None, "FC rejected request (error frame)"

        payload_len = buf[idx + 3]
        if len(buf) < idx + 6 + payload_len:
            continue

        resp_code = buf[idx + 4]
        payload = buf[idx + 5:idx + 5 + payload_len]
        crc = buf[idx + 5 + payload_len]

        # Verify XOR checksum
        calc_crc = payload_len ^ resp_code
        for b in payload:
            calc_crc ^= b

        if crc != calc_crc:
            return None, "Checksum error"

        return payload, None

    return None, "Timeout (FC did not respond to MSP request)"


def main():
    parser = argparse.ArgumentParser(description="Read live FC telemetry and RC channels over MSP v1.")
    parser.add_argument("--samples", "-s", type=int, default=1, help="Number of RC samples to record (default: 1)")
    parser.add_argument("--interval", "-i", type=float, default=0.2, help="Sampling interval in seconds (default: 0.2)")
    parser.add_argument("--port", "-p", help="Serial port device")
    parser.add_argument("--serial", help="USB serial number of Flight Controller")

    args = parser.parse_args()

    port = find_fc_port(target_port=args.port, target_serial=args.serial)
    print(f"# Connecting via MSP to {port}...", file=sys.stderr)

    try:
        ser = serial.Serial(port, 115200, timeout=0.2)
    except serial.SerialException as err:
        raise SystemExit(f"Failed to open port {port}: {err}")

    with ser:
        ser.dtr = True
        time.sleep(0.4)

        # 1. API Version
        payload, err = msp_request(ser, MSP_API_VERSION)
        if err:
            print(f"MSP_API_VERSION : FAILED ({err})")
            print("Note: If MSP times out, FC may be stuck in CLI mode. Run `python tools/bf_cli.py \"status\"` or replug USB.")
            sys.exit(1)
        else:
            api_ver = f"{payload[0]}.{payload[1]}.{payload[2]}" if len(payload) >= 3 else payload.hex()
            print(f"MSP_API_VERSION : {api_ver}")

        # 2. FC Status
        payload, err = msp_request(ser, MSP_STATUS)
        if err:
            print(f"MSP_STATUS      : FAILED ({err})")
        else:
            print(f"MSP_STATUS      : OK ({len(payload)} bytes received)")

        # 3. Read RC Channels
        print(f"\nSampling RC channels ({args.samples} sample(s)):")
        for sample_idx in range(args.samples):
            payload, err = msp_request(ser, MSP_RC)
            if err:
                print(f"Sample {sample_idx+1}: MSP_RC FAILED ({err})")
                break

            channels = struct.unpack("<" + "H" * (len(payload) // 2), payload)
            names = ["Roll", "Pitch", "Yaw", "Thr"] + [f"AUX{i}" for i in range(1, len(channels) - 3)]

            if sample_idx == 0:
                print("  " + "  ".join(f"{n:>6}" for n in names))

            print("  " + "  ".join(f"{v:>6}" for v in channels))

            if sample_idx < args.samples - 1:
                time.sleep(args.interval)


if __name__ == "__main__":
    main()
