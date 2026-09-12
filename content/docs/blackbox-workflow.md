---
title: "Blackbox Extraction & Log Analysis Guide"
date: 2026-09-12T10:00:00Z
draft: false
---

# Blackbox Extraction & Log Analysis Guide

Onboard SPI flash on 1S/2S AIO Flight Controllers records high-frequency gyro ADC readings, motor commands, DShot telemetry eRPM, and PID term states during flight.

---

## 1. Extracting `.bbl` Files over USB Mass Storage (`msc`)

Rather than downloading logs slowly over serial MSP, Betaflight can reboot into USB Mass Storage Mode:

```bash
# Check flash usage first
python tools/blackbox_tool.py --info

# Reboot FC into Mass Storage Mode
python tools/blackbox_tool.py --msc
```

The Flight Controller re-enumerates as a USB mass storage flash drive labelled `BETAFLT`.

Copy logs using `tools/blackbox_tool.py`:
```bash
python tools/blackbox_tool.py --copy
```

This automatically locates `BETAFLT` on Windows (`E:\`), macOS (`/Volumes/BETAFLT`), or Linux (`/run/media/...`), and copies all `btfl_*.bbl` files to `logs/`.

---

## 2. Understanding Blackbox Sample Rates & Decimation

By default, Betaflight uses `blackbox_sample_rate = 1/4`, recording 1 out of every 4 gyro loop iterations to conserve onboard flash space.

When decoding with `blackbox_decode`:
```text
2 frames failed to decode.
92175 iterations are missing in total (75.01%).
```

> [!NOTE]
> **This is expected behavior.** Under `1/4` decimation, 75% of loop iterations were never logged by design. It is not data corruption.
> 
> Effective logging frequency under an 8 kHz gyro loop with `1/4` decimation is **~1 kHz**, providing a Nyquist frequency ceiling of **500 Hz** for noise analysis.

---

## 3. Deriving Analytical Metrics from CSV

### Motor Balance Ratios
Divide the mean `eRPM[n]` by the mean `motor[n]` command across all 4 motors for samples above idle throttle:

$$\text{Balance Ratio}_n = \frac{\text{Mean}(eRPM_n)}{\text{Mean}(MotorOutput_n)}$$

- **Healthy Craft**: All 4 motor ratios stay within a 3% spread.
- **Faulty Craft**: An outlier ratio indicates a cold solder joint, damaged motor winding, or slipping prop.
