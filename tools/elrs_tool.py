#!/usr/bin/env python3
"""WhoopShop ExpressLRS (ELRS) Receiver Helper Tool.

Inspects and configures ExpressLRS (CRSF) receiver settings, serial RX provider,
channel map, and telemetry ratios on Betaflight flight controllers.

Usage:
    python tools/elrs_tool.py --info
    python tools/elrs_tool.py --apply-crsf
"""
import argparse
import sys

try:
    from tools.bf_cli import execute_cli, find_fc_port
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import execute_cli, find_fc_port


def get_elrs_info(port=None):
    port = find_fc_port(target_port=port)
    print("# Querying ExpressLRS / Receiver CLI settings...", file=sys.stderr)
    execute_cli(port, [
        "get serialrx_provider",
        "get rx_serial_protocol",
        "get map",
        "get crsf_use_painless_telemetry",
        "get telemetry_disabled",
    ])


def apply_crsf_preset(port=None):
    port = find_fc_port(target_port=port)
    print("# Applying ExpressLRS (CRSF + AETR11) receiver preset...", file=sys.stderr)
    execute_cli(port, [
        "feature TELEMETRY",
        "feature RX_SERIAL",
        "set serialrx_provider = CRSF",
        "set map = AETR11",
    ], save=True)
    print("\n[+] ExpressLRS receiver settings applied and saved!")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop ExpressLRS Receiver Helper Tool.")
    parser.add_argument("--info", action="store_true", help="Query current RX provider and channel map")
    parser.add_argument("--apply-crsf", action="store_true", help="Apply CRSF receiver provider & AETR11 channel map")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.apply_crsf:
        apply_crsf_preset(args.port)
    else:
        get_elrs_info(args.port)


if __name__ == "__main__":
    main()
