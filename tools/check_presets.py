#!/usr/bin/env python3
"""Validate every canned command list in this workspace against bf_vars.

Runs in CI with no flight controller attached. It exists because a wrong
variable name is invisible at runtime: Betaflight prints `Invalid name` and
carries on, so a preset can appear to apply while silently doing nothing.

Usage:
    python -m tools.check_presets
"""
import os
import sys

try:
    from tools.bf_vars import validate
    from tools.tuning_tool import PRESETS
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tools.bf_vars import validate
    from tools.tuning_tool import PRESETS

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Checked-in CLI scripts users are told to apply to their board. A wrong name
# here is as damaging as one in a preset, and just as invisible at runtime.
CONFIG_FILES = [
    os.path.join("config", "baseline_diff.txt"),
]


def read_cli_file(path):
    """Return the command lines from a CLI script, dropping comments."""
    with open(path, encoding="utf-8") as handle:
        return [
            line.strip() for line in handle
            if line.strip() and not line.strip().startswith("#")
        ]


def collect():
    """Return {source label: [commands]} for every hard-coded command list."""
    groups = {}
    for name, preset in PRESETS.items():
        groups[f"tuning_tool preset '{name}'"] = list(preset["commands"])

    for relative in CONFIG_FILES:
        path = os.path.join(REPO_ROOT, relative)
        if os.path.exists(path):
            groups[relative] = read_cli_file(path)

    return groups


def main():
    failures = 0
    for label, commands in sorted(collect().items()):
        problems = validate(commands)
        if problems:
            failures += 1
            print(f"FAIL  {label}")
            for problem in problems:
                print(f"        {problem}")
        else:
            print(f"ok    {label} ({len(commands)} commands)")

    if failures:
        print(f"\n{failures} command list(s) contain names the flight controller will reject.")
        return 1

    print("\nAll command lists use valid Betaflight variable names.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
