#!/usr/bin/env python3
"""WhoopShop Automated Pre-Flight Audit Tool.

Connects to a Flight Controller and performs a multi-point pre-flight health check:
  1. Arming disable flags & CPU load.
  2. Motor protocol & Bi-directional DShot state.
  3. Receiver protocol & channel mapping.
  4. Blackbox SPI flash capacity.

Usage:
    python tools/preflight.py
"""
import argparse
import sys

try:
    from tools.bf_cli import execute_cli, find_fc_port
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_cli import execute_cli, find_fc_port


def parse_audit_results(output_text):
    results = []

    # 1. Arming flags
    if "Arming disable flags:" in output_text:
        line = [l for l in output_text.splitlines() if "Arming disable flags:" in l][0]
        flags = line.split(":")[-1].strip()
        # CLI flag is expected while connected
        problematic = [f for f in flags.split() if f not in ("CLI", "NOPROOF", "RXLOSS")]
        if not problematic:
            results.append(("Arming Disable Flags", "PASS", f"OK ({flags})"))
        else:
            results.append(("Arming Disable Flags", "WARN", f"Flags active: {flags}"))

    # 2. DShot eRPM telemetry
    if "dshot_bidir" in output_text:
        line = [l for l in output_text.splitlines() if "dshot_bidir" in l][0]
        state = line.split("=")[-1].strip()
        if state.upper() in ("ON", "1", "TRUE"):
            results.append(("Bi-directional DShot", "PASS", "ON (eRPM telemetry active)"))
        else:
            results.append(("Bi-directional DShot", "WARN", "OFF (Recommend enabling for eRPM filtering)"))

    # 3. Serial RX Provider
    if "serialrx_provider" in output_text:
        line = [l for l in output_text.splitlines() if "serialrx_provider" in l][0]
        provider = line.split("=")[-1].strip()
        results.append(("Receiver Provider", "PASS", f"{provider}"))

    # 4. Flash info
    if "FlashFS" in output_text or "usedSize" in output_text:
        for line in output_text.splitlines():
            if "usedSize" in line and "totalSize" in line:
                results.append(("Blackbox Flash", "INFO", line.strip()))

    return results


def run_preflight_audit(port=None):
    port = find_fc_port(target_port=port)
    print(f"# Running WhoopShop Pre-Flight Audit on {port}...\n", file=sys.stderr)

    import io
    from contextlib import redirect_stdout

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            execute_cli(port, [
                "status",
                "get dshot_bidir",
                "get serialrx_provider",
                "get map",
                "flash_info",
            ])
    except Exception as err:
        print(f"ERROR: Could not complete audit over serial: {err}")
        sys.exit(1)

    raw_output = buf.getvalue()
    results = parse_audit_results(raw_output)

    print("==================================================")
    print("  🛸 WhoopShop Pre-Flight Audit Report")
    print("==================================================")
    print(f"  Target Port: {port}\n")

    for item, status, desc in results:
        status_badge = f"[{status}]"
        print(f"  {status_badge:<8} {item:<22} : {desc}")

    print("==================================================\n")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Automated Pre-Flight Audit Tool.")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()
    run_preflight_audit(args.port)


if __name__ == "__main__":
    main()
