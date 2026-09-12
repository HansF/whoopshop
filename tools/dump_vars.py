#!/usr/bin/env python3
"""Generate the Betaflight variable table from a connected flight controller.

`get` with no argument makes the firmware print every setting it has, with its
current value and its constraint (an enum's allowed values, an integer's range,
or a string's length). That is the authoritative list for the firmware actually
on the board, so the table is read from hardware rather than hand-maintained.

    python tools/dump_vars.py                  # regenerate the table
    python tools/dump_vars.py --print          # show a summary, write nothing

The result is written to tools/bf_vars_table.py and consumed by tools/bf_vars.py.
Regenerate it after a firmware update, or to match a different board.
"""
import argparse
import datetime
import os
import re
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from tools.fc_session import CliSession

TABLE_PATH = os.path.join(_REPO_ROOT, "tools", "bf_vars_table.py")
REFERENCE_PATH = os.path.join(
    _REPO_ROOT, "content", "reference", "all-cli-variables.md")

# A profile-scoped variable prints its scope between the value and the
# constraint, so this line must not be read as the end of the variable's block.
SCOPE_LINE = re.compile(r"^(profile|rateprofile|battery_profile)\s+\d+$")
VALID_NAME = re.compile(r"[a-z0-9_]+")


def parse_get_all(text):
    """Parse the output of a bare `get` into {name: {kind, constraints}}."""
    variables = {}
    current = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        if SCOPE_LINE.match(line):
            if current:
                variables[current]["scope"] = line.split()[0]
            continue

        if line.startswith("Allowed values:"):
            if current:
                values = [v.strip() for v in line.split(":", 1)[1].split(",")]
                variables[current]["values"] = [v for v in values if v]
        elif line.startswith("Allowed range:"):
            if current:
                match = re.search(r"(-?\d+)\s*-\s*(-?\d+)", line.split(":", 1)[1])
                if match:
                    variables[current]["min"] = int(match.group(1))
                    variables[current]["max"] = int(match.group(2))
        elif line.startswith("String length:"):
            if current:
                match = re.search(r"(\d+)\s*-\s*(\d+)", line)
                if match:
                    variables[current]["kind"] = "string"
                    variables[current]["minlen"] = int(match.group(1))
                    variables[current]["maxlen"] = int(match.group(2))
        elif line.startswith("Array length:"):
            if current:
                variables[current]["kind"] = "array"
        elif line.startswith("Default value:"):
            if current:
                variables[current]["default"] = line.split(":", 1)[1].strip()
        elif "=" in line:
            name = line.partition("=")[0].strip()
            if VALID_NAME.fullmatch(name):
                current = name
                variables[name] = {}
            else:
                current = None
        else:
            current = None

    for entry in variables.values():
        if entry.get("kind"):
            continue
        if "values" in entry:
            entry["kind"] = "enum"
        elif "min" in entry:
            entry["kind"] = "int"
        else:
            entry["kind"] = "array"

    return variables


def firmware_line(version_text):
    for line in version_text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped.startswith("Betaflight /"):
            return stripped
    return "unknown"


def render(variables, firmware):
    """Render the table as an importable Python module."""
    out = [
        '"""Betaflight variable table, generated from a live flight controller.',
        "",
        "DO NOT EDIT BY HAND. Regenerate with:",
        "",
        "    python tools/dump_vars.py",
        "",
        f"Source firmware: {firmware}",
        f"Generated: {datetime.date.today().isoformat()}",
        "",
        "Each entry carries the variable's kind and its constraint, so a value",
        "can be checked before it is sent as well as the name.",
        '"""',
        "",
        f'FIRMWARE = {firmware!r}',
        f'GENERATED = {datetime.date.today().isoformat()!r}',
        "",
        "VARIABLES = {",
    ]
    for name in sorted(variables):
        entry = variables[name]
        parts = [f'"kind": {entry["kind"]!r}']
        if "values" in entry:
            parts.append(f'"values": {entry["values"]!r}')
        if "min" in entry:
            parts.append(f'"min": {entry["min"]!r}, "max": {entry["max"]!r}')
        if "minlen" in entry:
            parts.append(f'"minlen": {entry["minlen"]!r}, "maxlen": {entry["maxlen"]!r}')
        if "scope" in entry:
            parts.append(f'"scope": {entry["scope"]!r}')
        out.append(f'    {name!r}: {{{", ".join(parts)}}},')
    out.append("}")
    out.append("")
    return "\n".join(out)


def render_reference(variables, firmware):
    """Render every variable as a Markdown page for the local workshop site."""
    scoped = {"profile": "PID profile", "rateprofile": "rate profile",
              "battery_profile": "battery profile"}

    lines = [
        "---",
        'title: "Complete CLI Variable Reference"',
        "draft: false",
        "tags: [cli, reference, generated]",
        "---",
        "",
        f"Every setting exposed by `{firmware}`.",
        "",
        "Generated from a connected flight controller with "
        "`python tools/dump_vars.py`. Regenerate it after a firmware update, "
        "or to match a different board.",
        "",
        f"**{len(variables)} variables.** A variable marked with a profile is "
        "stored per profile, so switching profiles changes its value.",
        "",
        "| Variable | Type | Allowed | Profile |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for name in sorted(variables):
        entry = variables[name]
        kind = entry["kind"]
        if kind == "enum":
            allowed = ", ".join(f"`{v}`" for v in entry["values"])
        elif kind == "int":
            allowed = f"{entry['min']} to {entry['max']}"
        elif kind == "string":
            allowed = f"{entry['minlen']} to {entry['maxlen']} characters"
        else:
            allowed = "array"
        scope = scoped.get(entry.get("scope", ""), "")
        lines.append(f"| `{name}` | {kind} | {allowed} | {scope} |")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate the Betaflight variable table from a connected FC.")
    parser.add_argument("--port", help="Serial port device")
    parser.add_argument("--print", dest="preview", action="store_true",
                        help="Summarise what was read without writing the table")
    parser.add_argument("--reference", action="store_true",
                        help="Also write the Markdown reference page for the local site")
    args = parser.parse_args()

    with CliSession(port=args.port) as fc:
        print("# Reading every setting from the flight controller...", file=sys.stderr)
        version = fc.run("version")
        dump = fc.run("get", timeout=180.0)

    variables = parse_get_all(dump)
    firmware = firmware_line(version)

    if not variables:
        print("ERROR: the flight controller returned no settings.")
        sys.exit(1)

    kinds = {}
    for entry in variables.values():
        kinds[entry["kind"]] = kinds.get(entry["kind"], 0) + 1

    print(f"Firmware  : {firmware}")
    print(f"Variables : {len(variables)}")
    for kind in sorted(kinds):
        print(f"  {kind:<8}: {kinds[kind]}")

    if args.preview:
        return

    with open(TABLE_PATH, "w", encoding="utf-8") as handle:
        handle.write(render(variables, firmware))
    print(f"\n[+] Wrote {TABLE_PATH}")

    if args.reference:
        os.makedirs(os.path.dirname(REFERENCE_PATH), exist_ok=True)
        with open(REFERENCE_PATH, "w", encoding="utf-8") as handle:
            handle.write(render_reference(variables, firmware))
        print(f"[+] Wrote {REFERENCE_PATH}")


if __name__ == "__main__":
    main()
