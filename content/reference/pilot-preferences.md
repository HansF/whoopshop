---
title: "Pilot Preferences — HansF Standard Setup"
date: 2026-09-12T19:30:00Z
draft: false
tags: [setup, modes, rates, reference]
---

# Pilot Preferences — HansF Standard Setup

The switch layout, rates and throttle feel used on every craft in this workshop.
Apply this to a new drone and it will fly like the rest of the fleet. Everything
here is pilot preference. Nothing on this page is frame or motor specific, so it is
safe to paste onto any board.

Established on Crafty and ported to the Air65 on 2026-09-12.

---

## Switch Layout

| Mode | Box ID | Channel | Range |
| :--- | :--- | :--- | :--- |
| **Arm** | 0 | AUX4 | `1800`–`2100` |
| **Angle** | 1 | AUX2 | `900`–`1300` |
| **Horizon** | 2 | AUX2 | `1300`–`1700` |
| **Beeper** | 13 | AUX1 | `1700`–`2100` |
| **Crashflip** | 35 | AUX5 | `1700`–`2100` |
| **Blackbox** | 26 | AUX1 | `900`–`2100` |
| **OSD profile** | adjustment 29 | AUX3 | `900`–`2100` |

Arm deliberately uses a narrow `1800`–`2100` window rather than the more common
`1700`–`2100`. Angle and horizon share AUX2 as a three-position switch, with acro
in the top position.

---

## Rates

Rate type is **ACTUAL**. This is the firmware default on Betaflight 2026.6, so it
never appears in a `diff` — a craft showing `set rates_type = BETAFLIGHT` has not
been converted yet.

| Axis | Centre Sensitivity | Maximum Rate | Expo |
| :--- | :--- | :--- | :--- |
| **Roll** | 170 °/s | 550 °/s | 0.35 |
| **Pitch** | 170 °/s | 550 °/s | 0.35 |
| **Yaw** | 120 °/s | 400 °/s | 0.25 |

---

## Throttle & Controls

| CLI Variable | Value | Description |
| :--- | :--- | :--- |
| `set thr_mid = 40` | `40` | Throttle curve midpoint |
| `set thr_expo = 35` | `35` | Softens the low half of the throttle stick |
| `set thr_hover = 44` | `44` | Hover point for the OSD estimate |
| `set throttle_limit_type = SCALE` | `SCALE` | Scale rather than clip |
| `set throttle_limit_percent = 80` | `80` | Caps usable throttle at 80% |
| `set fpv_mix_degrees = 10` | `10` | Yaw mix for the camera uptilt |

Channel map stays at the default `AETR1234`.

---

## Apply to a New Craft

Back up first, then paste the block below. Nothing here touches the PID profile,
the filter stack, board alignment or accelerometer calibration.

```bash
python tools/backup_restore.py --backup --name <craft>_factory
```

```bash
python tools/bf_cli.py --save \
  "aux 0 0 3 1800 2100 0 0" \
  "aux 1 1 1 900 1300 0 0" \
  "aux 2 2 1 1300 1700 0 0" \
  "aux 3 13 0 1700 2100 0 0" \
  "aux 4 0 0 900 900 0 0" \
  "aux 5 35 4 1700 2100 0 0" \
  "aux 6 26 0 900 2100 0 0" \
  "adjrange 0 0 2 900 2100 29 2 0 0" \
  "feature TELEMETRY" \
  "set pilot_name = HansF" \
  "set fpv_mix_degrees = 10" \
  "set crashflip_rate = 30" \
  "set crashflip_auto_rearm = ON" \
  "set vtx_low_power_disarm = ON" \
  "rateprofile 0" \
  "set rates_type = ACTUAL" \
  "set roll_rc_rate = 17" "set pitch_rc_rate = 17" "set yaw_rc_rate = 12" \
  "set roll_expo = 35"   "set pitch_expo = 35"    "set yaw_expo = 25" \
  "set roll_srate = 55"  "set pitch_srate = 55"   "set yaw_srate = 40" \
  "set thr_mid = 40" "set thr_expo = 35" "set thr_hover = 44" \
  "set throttle_limit_type = SCALE" "set throttle_limit_percent = 80"
```

> [!CAUTION]
> Never copy `vcd_video_system` or `osd_displayport_device` between craft. BETAFPV
> boards need them pinned to `NTSC` and `MAX7456` or the OSD goes blank. See
> [BETAFPV FC Gyroscope & Firmware Notes](/reference/betafpv-fc-gyro-firmware-notes.html).

> [!CAUTION]
> `aux 4 0 0 900 900 0 0` clears slot 4. Many factory configurations park crashflip
> there, and leaving it would give you two crashflip switches.

---

## Verification

```bash
python tools/bf_cli.py "diff"
```

The `aux`, `adjrange` and `rateprofile 0` blocks should match this page exactly, and
`rates_type` should be **absent** from the output. With the radio on and props off,
`python tools/bf_msp.py --samples 10` confirms each switch lands in its intended range.
