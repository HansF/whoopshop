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
    from tools.fc_session import CliSession
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.fc_session import CliSession

AUDIT_COMMANDS = [
    "status",
    "get dshot_bidir",
    "get serialrx_provider",
    "map",
    "flash_info",
]


def _value(output):
    """Pull the value from a `get name = value` reply."""
    for line in output.splitlines():
        if "=" in line and not line.lower().startswith("allowed"):
            return line.split("=", 1)[1].strip()
    return output.strip()


def parse_audit_results(results):
    """Turn a {command: output} map into (item, status, detail) rows."""
    rows = []

    status_text = results.get("status", "")
    for line in status_text.splitlines():
        if "Arming disable flags:" in line:
            flags = line.split(":", 1)[1].strip()
            # CLI and MSP are expected while a USB session is open.
            blocking = [f for f in flags.split() if f not in ("CLI", "MSP")]
            if blocking:
                rows.append(("Arming Disable Flags", "WARN", f"Blocking: {' '.join(blocking)}"))
            else:
                rows.append(("Arming Disable Flags", "PASS", f"OK ({flags})"))
        elif line.startswith("CPU:"):
            rows.append(("System Load", "INFO", line.strip()))

    if "get dshot_bidir" in results:
        state = _value(results["get dshot_bidir"]).upper()
        if state in ("ON", "1", "TRUE"):
            rows.append(("Bi-directional DShot", "PASS", "ON (eRPM telemetry active)"))
        else:
            rows.append(("Bi-directional DShot", "WARN",
                         f"{state} (enable for RPM filtering)"))

    if "get serialrx_provider" in results:
        rows.append(("Receiver Provider", "PASS", _value(results["get serialrx_provider"])))

    if "map" in results:
        mapping = results["map"].strip().splitlines()
        if mapping:
            rows.append(("Channel Map", "INFO", mapping[-1].strip()))

    flash_text = results.get("flash_info", "")
    for line in flash_text.splitlines():
        if "usedSize" in line:
            rows.append(("Blackbox Flash", "INFO", line.strip()))
            break

    return rows


def run_preflight_audit(port=None):
    with CliSession(port=port) as fc:
        print(f"# Running WhoopShop Pre-Flight Audit on {fc.port}...\n", file=sys.stderr)
        results = fc.run_many(AUDIT_COMMANDS)
        resolved_port = fc.port

    rows = parse_audit_results(results)

    print("==================================================")
    print("  🛸 WhoopShop Pre-Flight Audit Report")
    print("==================================================")
    print(f"  Target Port: {resolved_port}\n")

    for item, status, detail in rows:
        print(f"  [{status}]{'':<{max(0, 6 - len(status))}} {item:<22} : {detail}")

    warnings = sum(1 for _, status, _ in rows if status == "WARN")
    print("==================================================")
    if warnings:
        print(f"  {warnings} warning(s). Review before flying.\n")
    else:
        print("  No warnings.\n")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Automated Pre-Flight Audit Tool.")
    parser.add_argument("--port", help="Serial port device")

    args = parser.parse_args()
    run_preflight_audit(args.port)


if __name__ == "__main__":
    main()
