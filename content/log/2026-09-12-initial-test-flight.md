---
title: "Baseline Hover & Flight Test"
date: 2026-09-12T10:00:00Z
craft_name: "WHOOP_SHOP_01"
battery_voltage: "1S LiHV 300mAh"
log_file: "btfl_001.bbl"
draft: false
tags: [blackbox, tuning]
---

## Flight Overview

- **Objectives**: Initial bench test, motor direction check, baseline hover stability.
- **Flight Duration**: 2m 45s
- **Location**: Indoor Workshop

## Telemetry Summary

| Parameter | Value |
| :--- | :--- |
| **Craft Name** | `WHOOP_SHOP_01` |
| **Firmware** | Betaflight 4.5.1 |
| **Motor Protocol** | DShot300 (Bi-directional DShot ON) |
| **Blackbox Sample Rate** | 1/4 (1 kHz effective sampling) |

## Blackbox Metrics

- **Motor Balance Ratios**:
  - Motor 1: `1.72`
  - Motor 2: `1.71`
  - Motor 3: `1.73`
  - Motor 4: `1.70`
  - *Analysis*: Ratios tightly grouped within 2% spread. No motor strain or cold joints detected.
- **Gyro Noise Floor**: Clean broadband response below 160 Hz.

## Pilot Notes

Initial hover was exceptionally smooth. DShot telemetry confirmed zero packet errors. Ready for high-rate outdoor flight testing.
