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
    from tools.bf_vars import check_responses
    from tools.fc_session import CliSession
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_vars import check_responses
    from tools.fc_session import CliSession


def get_elrs_info(port=None):
    """Report receiver provider, channel map, and telemetry state.

    `map` is a bare CLI command, not a variable, so it is sent on its own.
    Telemetry is a feature flag rather than a setting, so it is read from
    the `feature` listing.
    """
    print("# Querying ExpressLRS / Receiver CLI settings...", file=sys.stderr)
    with CliSession(port=port) as fc:
        results = fc.run_many([
            "get serialrx_provider",
            "get serialrx_inverted",
            "get serialrx_halfduplex",
            "get crsf_use_negotiated_baud",
            "map",
            "feature",
        ])
    check_responses(results)

    for command, output in results.items():
        print(f"===== {command} =====")
        print(output)
        print()

    feature_line = results.get("feature", "")
    telemetry = "enabled" if "TELEMETRY" in feature_line.replace("-TELEMETRY", "") else "disabled"
    print(f"Telemetry: {telemetry}")


def apply_crsf_preset(port=None, channel_map="AETR1234"):
    """Set the receiver to CRSF with a standard AETR channel map."""
    print(f"# Applying ExpressLRS (CRSF + {channel_map}) receiver preset...",
          file=sys.stderr)
    with CliSession(port=port, save=True) as fc:
        results = fc.run_many([
            "feature TELEMETRY",
            "feature RX_SERIAL",
            "set serialrx_provider = CRSF",
            f"map {channel_map}",
        ])
    check_responses(results)
    print("\n[+] ExpressLRS receiver settings applied and saved!")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop ExpressLRS Receiver Helper Tool.")
    parser.add_argument("--info", action="store_true", help="Query current RX provider and channel map")
    parser.add_argument("--apply-crsf", action="store_true", help="Apply CRSF receiver provider and channel map")
    parser.add_argument("--channel-map", default="AETR1234", help="Channel map to apply (default: AETR1234)")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()

    if args.apply_crsf:
        apply_crsf_preset(args.port, channel_map=args.channel_map)
    else:
        get_elrs_info(args.port)


if __name__ == "__main__":
    main()
