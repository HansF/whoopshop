---
name: blackbox-analysis
description: Extract, decode, and analyze Betaflight Blackbox flight logs stored on onboard SPI flash across Linux, macOS, and Windows. Use when downloading .bbl logs, inspecting motor balance, checking gyro noise floor, or verifying flash capacity.
---

# Blackbox Analysis & Log Management Skill

This skill guides the extraction, decoding, and analysis of Blackbox flight recordings from onboard SPI flash using native tools in `tools/blackbox_tool.py`.

---

## 1. Check Flash Capacity & Usage

Check how much SPI flash is consumed by flight recordings:

```bash
python tools/blackbox_tool.py --info
```

Look at `usedSize` vs `totalSize`.

> [!WARNING]
> **Flash Full Behavior**: Betaflight Blackbox **stops logging when the flash is full**. It does NOT overwrite old logs. Once `usedSize == totalSize`, subsequent flights record nothing. Always erase the flash after extracting logs!

---

## 2. Extract Logs via USB Mass Storage (`msc`)

1. Trigger Mass-Storage Mode:
   ```bash
   python tools/blackbox_tool.py --msc
   ```
   The board reboots as a USB flash drive labelled `BETAFLT`.

2. Copy `.bbl` Files:
   ```bash
   python tools/blackbox_tool.py --copy
   ```
   This automatically detects the `BETAFLT` volume on Windows (`E:\`), macOS (`/Volumes/BETAFLT`), or Linux (`/run/media/...`), and copies all `btfl_*.bbl` files to `logs/`.

3. Return FC to Normal Mode:
   Unplug and replug the USB cable.

---

## 3. Decoding & Analysis

### Decode to CSV
If `blackbox_decode` is installed:
```bash
python tools/blackbox_tool.py --decode btfl_001.bbl
```

### Understanding Decoder Outputs
- **"75% of iterations missing"**: Under default `blackbox_sample_rate = 1/4`, 3 out of 4 loop iterations are omitted by design to save flash. **This is expected decimation, not data loss.**
- **Motor Balance Ratios**: Compute mean `eRPM[n]` divided by mean `motor[n]` across all 4 motors. Uniform ratios mean healthy motors and solder joints; a single outlier motor indicates a bad solder joint, damaged motor winding, or slipping prop.
- **Gyro Noise Floor**: Evaluate FFT power spectral density of `gyroADC` signals to identify frame resonances or electrical motor noise.

---

## 4. Erase Flash for Next Flight

```bash
python tools/blackbox_tool.py --erase
```
