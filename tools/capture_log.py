#!/usr/bin/env python3
"""WhoopShop Telemetry & Information Capture Tool.

Connects to a Flight Controller (via tools/bf_cli.py) or reads local logs,
and automatically generates a rich Markdown flight log entry in `content/log/`.

Usage:
    python tools/capture_log.py --title "PID Tuning Session 1"
    python tools/capture_log.py --title "Hover Test" --log-file "btfl_001.bbl"
    python tools/capture_log.py --dry-run
"""
import argparse
import datetime
import os
import re
import sys

try:
    from tools.analyze_log import analyze, format_markdown
    from tools.bf_vars import parse_get
    from tools.fc_session import CliSession
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.analyze_log import analyze, format_markdown
    from tools.bf_vars import parse_get
    from tools.fc_session import CliSession


def find_decoded_csv(log_file):
    """Locate the CSV that blackbox_decode wrote for a .bbl, if any.

    blackbox_decode names its output `<stem>.NN.csv`, one per flight in the
    file, so the first match is used.
    """
    if not log_file:
        return None

    logs_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    stem = os.path.splitext(os.path.basename(log_file))[0]

    if not os.path.isdir(logs_dir):
        return None

    candidates = sorted(
        name for name in os.listdir(logs_dir)
        if name.startswith(stem) and name.endswith(".csv")
    )
    return os.path.join(logs_dir, candidates[0]) if candidates else None


def blackbox_section(log_file):
    """Real motor and gyro metrics when a decoded log exists, else guidance."""
    csv_path = find_decoded_csv(log_file)
    if not csv_path:
        return (
            "- No decoded log analyzed. Produce one with:\n"
            "  ```bash\n"
            "  python tools/blackbox_tool.py --decode "
            f"{log_file or 'btfl_001.bbl'}\n"
            "  ```"
        )

    try:
        return format_markdown(analyze(csv_path))
    except Exception as err:
        return f"- Could not analyze `{os.path.basename(csv_path)}`: {err}"


def parse_version(output_text):
    """Pull firmware and board name from the CLI `version` reply.

    `status` carries neither. Betaflight prints them as:
        # Betaflight / STM32F7X2 (S7X2) 4.5.1 ... MSP API: 1.46
        # board: manufacturer_id: BEFH, board_name: BETAFPVG473
    """
    info = {}
    for line in output_text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped.startswith("Betaflight /"):
            info["firmware"] = stripped
        elif "board_name:" in stripped:
            info["board"] = stripped.split("board_name:", 1)[1].split(",")[0].strip()
    return info


def parse_cli_status(output_text):
    """Extract key metrics from CLI 'status' command output."""
    info = {
        "craft_name": "WHOOP_SHOP",
        "firmware": "Unknown",
        "board": "Unknown",
        "arming_flags": "None",
        "cpu_load": "Unknown",
    }

    for line in output_text.splitlines():
        if "MCU" in line or "Firmware" in line or "Betaflight" in line:
            info["firmware"] = line.strip()
        elif "Board:" in line or "Board name" in line:
            info["board"] = line.split(":")[-1].strip()
        elif "Arming disable flags:" in line:
            info["arming_flags"] = line.split(":")[-1].strip()
        elif "CPU Clock=" in line or "System Uptime" in line or "CPU:" in line:
            info["cpu_load"] = line.strip()

    return info


def capture_telemetry(port=None):
    """Read status and key settings from the FC and return parsed metrics."""
    try:
        with CliSession(port=port) as fc:
            results = fc.run_many([
                "status",
                "version",
                "get craft_name",
                "get blackbox_sample_rate",
                "get motor_pwm_protocol",
            ])
    except Exception as err:
        print(f"Warning: could not fetch live CLI telemetry: {err}", file=sys.stderr)
        results = {}

    metrics = parse_cli_status(results.get("status", ""))
    metrics.update(parse_version(results.get("version", "")))

    # Exact match matters here: `get craft_name` also returns
    # `osd_craft_name_pos`, and returns it first.
    craft = parse_get(results.get("get craft_name", ""), "craft_name")
    if craft:
        metrics["craft_name"] = craft

    return metrics


def slugify(text):
    """Convert text title to URL-safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


def create_log_entry(title, log_file="", dry_run=False, port=None):
    """Generate Markdown flight log page in content/log/."""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%S%z") or now.isoformat()
    slug = slugify(title) if title else "flight-log"
    filename = f"{date_str}-{slug}.md"

    metrics = capture_telemetry(port=port) if not dry_run else {
        "craft_name": "WHOOP_SHOP_DEMO",
        "firmware": "Betaflight 4.5.1",
        "board": "BETAFPVG473",
        "arming_flags": "ARMED / OK",
        "cpu_load": "CPU: 12%",
    }

    analysis = blackbox_section(log_file)

    markdown_content = f"""---
title: "{title}"
date: {date_str}
craft_name: "{metrics['craft_name']}"
board: "{metrics['board']}"
log_file: "{log_file}"
draft: false
---

## 1. Flight Overview & Objectives

- **Date & Time**: {date_str}
- **Target Craft**: `{metrics['craft_name']}` ({metrics['board']})
- **Blackbox Source Log**: `{log_file or 'N/A'}`

---

## 2. Captured Flight Controller Telemetry

| Telemetry Field | Captured Value |
| :--- | :--- |
| **Board / Firmware** | `{metrics['firmware']}` |
| **Arming Flags** | `{metrics['arming_flags']}` |
| **System Load** | `{metrics['cpu_load']}` |

---

## 3. Blackbox Analysis Findings

{analysis}

---

## 4. Pilot Notes & Adjustments

- *Notes recorded during session...*

```bash
# Example adjustment applied during this session
python tools/bf_cli.py --save "set craft_name = {metrics['craft_name']}"
```
"""

    content_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "log")
    os.makedirs(content_dir, exist_ok=True)
    target_filepath = os.path.join(content_dir, filename)

    if dry_run:
        print("--- DRY RUN: Generated Markdown Preview ---")
        print(markdown_content)
        print("------------------------------------------")
    else:
        with open(target_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"[+] Successfully captured telemetry and created log entry: `{target_filepath}`")

    return target_filepath


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Telemetry & Information Capture Tool.")
    parser.add_argument("--title", "-t", default="Flight Log", help="Title for the flight log entry")
    parser.add_argument("--log-file", "-l", default="", help="Associated .bbl file name (e.g. btfl_001.bbl)")
    parser.add_argument("--dry-run", action="store_true", help="Print preview without writing file")
    parser.add_argument("--port", "-p", help="Serial port device")

    args = parser.parse_args()

    create_log_entry(
        title=args.title,
        log_file=args.log_file,
        dry_run=args.dry_run,
        port=args.port,
    )


if __name__ == "__main__":
    main()
