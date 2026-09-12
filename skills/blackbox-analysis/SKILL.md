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

### Compute the Metrics
Do not work these out by hand. `tools/analyze_log.py` computes both:

```bash
python tools/analyze_log.py logs/btfl_001.01.csv
python tools/analyze_log.py logs/btfl_001.01.csv --markdown   # flight-log block
```

`tools/capture_log.py --log-file btfl_001.bbl` calls it automatically and
embeds the result in the generated log entry, so a decoded CSV in `logs/` is
all that is needed.

### Understanding Decoder Outputs
- **"75% of iterations missing"**: Under default `blackbox_sample_rate = 1/4`, 3 out of 4 loop iterations are omitted by design to save flash. **This is expected decimation, not data loss.**
- **Motor Balance Ratios**: Mean `eRPM[n]` divided by mean `motor[n]` for each motor. Uniform ratios mean healthy motors and solder joints. The tool reports each motor's deviation from the fleet mean and warns past 5%, which points at a cold solder joint, a damaged winding, a worn bearing, or a slipping prop. Ratios read `n/a` when bidirectional DShot was off, since the log then carries no eRPM.
- **Gyro Noise Floor**: Mean spectral magnitude above 100 Hz per axis. Below that threshold the signal is dominated by actual craft motion; what remains above it is frame resonance and electrical motor noise. Compare axes against each other and across flights rather than against an absolute number.

---

## 4. Erase Flash for Next Flight

```bash
python tools/blackbox_tool.py --erase
```
