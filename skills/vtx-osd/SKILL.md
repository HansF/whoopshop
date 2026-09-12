---
name: vtx-osd
description: Configure Video Transmitter (VTX) channels, power levels, pit mode, and On-Screen Display (OSD) layout elements on Betaflight flight controllers.
---

# VTX & OSD Management Skill

Use this skill when setting up analog VTX channels (RACEBAND, FATSHARK), power output levels (25mW, 100mW, 400mW), or positioning OSD display items.

---

## 1. Inspect VTX & OSD Settings

Query current VTX and OSD configuration:

```bash
python tools/vtx_osd_tool.py --info
```

---

## 2. Change VTX Channel or Power Level

```bash
# Set VTX to Raceband Channel 8 (5880 MHz) at 25mW
python tools/vtx_osd_tool.py --band RACEBAND --channel 8 --power 25

# Enable Pit Mode (reduces VTX output to minimum for pit safety)
python tools/vtx_osd_tool.py --pitmode ON
```

---

## 3. OSD Layout Standard

Standard 1S Whoop OSD layout positions:

| OSD Item | Position Variable | Typical Value |
| :--- | :--- | :--- |
| **Craft Name** | `osd_craft_name_pos` | `2058` (Top Left) |
| **Battery Voltage** | `osd_vbat_pos` | `2433` (Bottom Right) |
| **RSSI / dBm** | `osd_rssi_dbm_pos` | `2081` (Top Right) |
| **Warnings** | `osd_warnings_pos` | `14465` (Center Warning Banner) |
