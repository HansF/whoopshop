---
name: preflight-check
description: Perform automated pre-flight diagnostic audits on connected Flight Controllers. Checks arming disable flags, receiver endpoints, DShot telemetry, battery voltage, and Blackbox flash capacity.
---

# Pre-Flight Audit Skill

Use this skill before test flying to verify that the quad is healthy, free of arming flags, and safe for flight.

---

## 1. Run Automated Pre-Flight Audit

Execute the audit tool:

```bash
python tools/preflight.py
```

---

## 2. Audit Checklist Items

1. **Arming Disable Flags**:
   - Verify arming disable flags (e.g. `RXLOSS`, `CLI`, `ANGLE`, `CALIB`).
   - Normal when connected on bench over USB: `CLI` (clears on exit) and `RXLOSS` (if transmitter is off).
   - Problematic flags: `ACC_FAIL`, `CALIB`, `FAILSAFE`, `MOTOR_PROTO`.
2. **Receiver Signal & Endpoints**:
   - Midpoint: ~1500 (Roll, Pitch, Yaw).
   - Range: 1000 to 2000.
3. **DShot & Telemetry**:
   - Bi-directional DShot enabled (`dshot_bidir = ON`).
   - Motor poles set to 12 for 0802/0702 motors.
4. **Blackbox Storage**:
   - Flash space check (warns if flash >90% full).

---

## 3. Pre-Flight Audit Report Output

The tool prints a formatted summary table:

```text
==================================================
  WhoopShop Pre-Flight Audit Report
==================================================
  [PASS] Flight Controller Serial Link (COM3)
  [PASS] Arming Flags: OK (Bench USB active)
  [PASS] DShot Protocol: DSHOT300 (Bi-directional ON)
  [PASS] Receiver Protocol: CRSF (Channel Map AETR11)
  [WARN] Blackbox Flash: 85% full (Recommend erase before next flight)
==================================================
```
