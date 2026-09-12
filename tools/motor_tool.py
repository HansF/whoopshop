#!/usr/bin/env python3
"""WhoopShop Motor & ESC Diagnostic Helper Tool.

Inspects motor configuration, DShot telemetry protocols, motor poles,
and performs safe motor output spin checks (strictly requiring --props-off confirmation).

Usage:
    python tools/motor_tool.py --info
    python tools/motor_tool.py --test-motor 1 --props-off
"""
import argparse
import sys
import time

try:
    from tools.bf_cli import execute_cli, find_fc_port
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import execute_cli, find_fc_port


def get_motor_info(port=None):
    port = find_fc_port(target_port=port)
    print("# Querying Motor & ESC configuration...", file=sys.stderr)
    execute_cli(port, [
        "get motor_pwm_protocol",
        "get dshot_bidir",
        "get motor_poles",
        "get dynamic_idle_min_rpm",
    ])


def test_motor_spin(motor_id, props_off=False, port=None):
    if not props_off:
        print("ERROR: Safety check failed!")
        print("Motor testing requires explicit confirmation that all propellers have been removed.")
        print(f"Run: python tools/motor_tool.py --test-motor {motor_id} --props-off")
        sys.exit(1)

    port = find_fc_port(target_port=port)
    print(f"\n[!] PROPS OFF CONFIRMED. Testing Motor {motor_id} at low throttle (1050 / ~5%) on {port}...")

    # We use CLI motor testing or motor command
    execute_cli(port, [
        f"motor {motor_id} 1050",
    ])
    time.sleep(1.5)
    execute_cli(port, [
        f"motor {motor_id} 1000",
    ])
    print(f"\n[+] Motor {motor_id} test sequence complete.")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Motor & ESC Diagnostic Helper Tool.")
    parser.add_argument("--info", action="store_true", help="Query motor settings, DShot protocol, and motor poles")
    parser.add_argument("--test-motor", type=int, choices=[1, 2, 3, 4], help="Test spin motor ID (1-4)")
    parser.add_argument("--props-off", action="store_true", help="Safety flag confirming all propellers are removed")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.test_motor:
        test_motor_spin(args.test_motor, props_off=args.props_off, port=args.port)
    else:
        get_motor_info(args.port)


if __name__ == "__main__":
    main()
