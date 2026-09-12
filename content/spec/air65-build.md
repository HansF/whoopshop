---
title: "BetaFPV Air65 Build Spec"
date: 2026-09-12T19:30:00Z
craft_name: "AIR65 F"
draft: false
tags: [hardware, setup, rates, modes, osd]
---

## Hardware Specification

- **Airframe**: BetaFPV Air65 65mm Brushless Whoop
- **Flight Controller**: BETAFPV G473 AIO V2 (`BETAFPVG473_V2`, `manufacturer_id BEFH`)
- **MCU / Gyro**: STM32G474xx @ 168 MHz / BMI270 (see the caution below)
- **Firmware**: Betaflight 2026.6.0-alpha (May 15 2026), MSP API 1.48
- **Motors**: 0802 Gemfan 1219S class (PID profile `GF 1219S`)
- **ESC Protocol**: DShot300, bi-directional DShot ON, 12 motor poles
- **Receiver**: Onboard serial ELRS, CRSF protocol, channel map `AETR1234`
- **Video Transmitter**: Onboard, MAX7456 OSD, NTSC, Raceband channel 1 (5658 MHz)
- **Blackbox**: 16 MB SPI flash (JEDEC `0x00852018`)
- **Board Orientation**: `align_board_yaw = -135`

> [!CAUTION]
> This board runs a **customized BETAFPV build of the Betaflight developer
> firmware** because its gyro is not yet supported by official releases. Do not
> flash stock Betaflight onto it, and use the development configurator at
> <https://master.app.betaflight.com/> rather than the release one. Full details in
> [BETAFPV FC Gyroscope & Firmware Notes](/reference/betafpv-fc-gyro-firmware-notes.html).

---

## Configuration Baseline

Set up on 2026-09-12 to match the pilot preferences carried over from
[Crafty](/log/2026-09-12-air65-setup.html). See
[Pilot Preferences](/reference/pilot-preferences.html) for the reusable block.

### Switch Layout

| Mode | Channel | Range | Notes |
| :--- | :--- | :--- | :--- |
| **Arm** | AUX4 | `1800`–`2100` | Deliberately narrow |
| **Angle** | AUX2 | `900`–`1300` | Low position |
| **Horizon** | AUX2 | `1300`–`1700` | Middle position |
| **Beeper** | AUX1 | `1700`–`2100` | |
| **Crashflip** | AUX5 | `1700`–`2100` | Auto-rearm ON, rate 30 |
| **Blackbox** | AUX1 | `900`–`2100` | Full range, always logging |
| **OSD profile** | AUX3 | `900`–`2100` | Adjustment function 29 |
| **VTX power** | AUX6 | 4 steps | 25 / 100 / 200 / 400 mW |

### Rates

Rate type is **ACTUAL**, which is the firmware default and therefore absent from `diff`.

| Axis | Centre Sensitivity | Maximum Rate | Expo |
| :--- | :--- | :--- | :--- |
| **Roll** | 170 °/s | 550 °/s | 0.35 |
| **Pitch** | 170 °/s | 550 °/s | 0.35 |
| **Yaw** | 120 °/s | 400 °/s | 0.25 |

### Throttle

| Variable | Value |
| :--- | :--- |
| `set thr_mid` | `40` |
| `set thr_expo` | `35` |
| `set thr_hover` | `44` |
| `set throttle_limit_type` | `SCALE` |
| `set throttle_limit_percent` | `80` |

---

## Left at Factory Settings

The PID profile, filter stack, board alignment and accelerometer calibration are
specific to this frame and motor combination and were **not** copied from Crafty.

- PID profile 0 `GF 1219S`: `p_pitch 56 / i_pitch 91 / d_pitch 44 / f_pitch 41`
- Filters: `gyro_lpf2_static_hz 600`, dynamic notch count 2, Q 500, 110–400 Hz
- `motor_idle = 550`, `dyn_idle_min_rpm = 30`
- `align_board_yaw = -135`, `acc_calibration = -2,-7,36,1`
