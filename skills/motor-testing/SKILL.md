---
name: motor-testing
description: Perform safe motor diagnostics, motor pole verification, DShot telemetry error rate checks, and spin direction tests. ALWAYS enforces PROPS OFF before testing.
---

# Motor & ESC Diagnostics Skill

Use this skill when diagnosing motor issues, cold solder joints, DShot packet error rates, or motor directions on micro Whoops.

> [!CAUTION]
> **PROPS OFF REQUIRED**: Never test motors while propellers are attached! Always confirm that all 4 props are removed before running motor diagnostics.

---

## 1. Inspect DShot Telemetry & Motor Settings

Query motor poles, DShot protocol, and bi-directional DShot configuration:

```bash
python tools/motor_tool.py --info
```

---

## 2. Test Individual Motor Outputs

To test motor spin outputs safely (requires explicit `--props-off` flag confirmation):

```bash
# Preview motor test parameters
python tools/motor_tool.py --test-motor 1

# Execute 2-second motor spin test at 10% throttle (props MUST be removed)
python tools/motor_tool.py --test-motor 1 --props-off
```

---

## 3. DShot Error Diagnostic Checklist

If DShot telemetry reports eRPM errors or non-zero packet drops:
1. **Check Soldering**: Inspect ESC motor pads for cold solder joints or loose motor wires.
2. **Bluejay PWM Frequency**: Verify ESC is flashed with Bluejay 48kHz (standard for 1S Whoops).
3. **Motor Pole Count**: Verify `motor_poles = 12` for 0802 / 0702 / 1102 brushless motors.
