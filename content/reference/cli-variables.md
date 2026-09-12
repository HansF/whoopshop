---
title: "Betaflight CLI Variables Cheat Sheet for 1S/2S Whoops"
date: 2026-09-12T10:00:00Z
draft: false
tags: [cli, reference]
---

# Betaflight CLI Variables Cheat Sheet for 1S/2S Whoops

Quick reference lookup for essential CLI configuration variables used in 1S and 2S Tiny Whoop tuning.

---

## Identity & General

| CLI Variable | Default / Typical | Description |
| :--- | :--- | :--- |
| `set craft_name = WHOOP` | `""` | Onscreen Display (OSD) craft identifier |
| `set osd_profile = 1` | `1` | Active OSD layout profile (1..3) |

---

## Motor & ESC Protocol

| CLI Variable | Typical 1S Whoop | Description |
| :--- | :--- | :--- |
| `set motor_pwm_protocol = DSHOT300` | `DSHOT300` | Motor signal protocol (Bluejay 48kHz recommended) |
| `set dshot_bidir = ON` | `ON` | Enable Bi-directional DShot eRPM telemetry |
| `set motor_poles = 12` | `12` | Magnet count (12 poles for 0802/0702 motors) |
| `set dyn_idle_min_rpm = 30` | `30` | Minimum motor RPM (3000 RPM) to prevent stalls |

---

## Blackbox Flash Logging

| CLI Variable | Typical 1S Whoop | Description |
| :--- | :--- | :--- |
| `set blackbox_device = SPIFLASH` | `SPIFLASH` | Onboard 16MB SPI flash storage |
| `set blackbox_sample_rate = 1/4` | `1/4` | Log 1 out of 4 loop iterations (~1 kHz effective) |
