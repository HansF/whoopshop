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
    from tools.bf_vars import check_responses
    from tools.fc_session import CliSession
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_vars import check_responses
    from tools.fc_session import CliSession

MOTOR_STOP = 1000


def get_motor_info(port=None):
    print("# Querying Motor & ESC configuration...", file=sys.stderr)
    with CliSession(port=port) as fc:
        results = fc.run_many([
            "get motor_pwm_protocol",
            "get dshot_bidir",
            "get motor_poles",
            "get dyn_idle_min_rpm",
            "get motor_idle",
        ])
    check_responses(results)

    for command, output in results.items():
        print(f"===== {command} =====")
        print(output)
        print()


def test_motor_spin(motor_id, props_off=False, port=None, throttle=1050, duration=1.5):
    """Spin one motor briefly, then stop it.

    The spin and the stop happen inside a single CLI session, with the stop in
    a `finally` block. An earlier version issued each in its own session, which
    meant an exception or a Ctrl-C between them left the motor running.
    """
    if not props_off:
        print("ERROR: Safety check failed!")
        print("Motor testing requires explicit confirmation that all propellers have been removed.")
        print(f"Run: python tools/motor_tool.py --test-motor {motor_id} --props-off")
        sys.exit(1)

    if not MOTOR_STOP < throttle <= 1200:
        print(f"ERROR: Refusing throttle {throttle}. Use a bench value between 1001 and 1200.")
        sys.exit(1)

    print(f"\n[!] PROPS OFF CONFIRMED. Testing motor {motor_id} at {throttle} for {duration}s...")

    with CliSession(port=port) as fc:
        try:
            fc.run(f"motor {motor_id} {throttle}")
            time.sleep(duration)
        finally:
            # Runs on success, on exception, and on KeyboardInterrupt. The
            # session's own `exit noreboot` is a second layer of protection,
            # since leaving CLI also clears the motor override.
            fc.run(f"motor {motor_id} {MOTOR_STOP}")
            print(f"[+] Motor {motor_id} commanded to stop ({MOTOR_STOP}).")

    print(f"[+] Motor {motor_id} test sequence complete.")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Motor & ESC Diagnostic Helper Tool.")
    parser.add_argument("--info", action="store_true", help="Query motor settings, DShot protocol, and motor poles")
    parser.add_argument("--test-motor", type=int, choices=[1, 2, 3, 4], help="Test spin motor ID (1-4)")
    parser.add_argument("--props-off", action="store_true", help="Safety flag confirming all propellers are removed")
    parser.add_argument("--throttle", type=int, default=1050, help="Bench throttle value 1001-1200 (default: 1050)")
    parser.add_argument("--duration", type=float, default=1.5, help="Spin duration in seconds (default: 1.5)")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.test_motor:
        test_motor_spin(args.test_motor, props_off=args.props_off, port=args.port,
                        throttle=args.throttle, duration=args.duration)
    else:
        get_motor_info(args.port)


if __name__ == "__main__":
    main()
