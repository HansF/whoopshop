---
title: "BETAFPV FC Gyroscope & Firmware Notes"
date: 2026-09-12T19:45:00Z
draft: false
---

# BETAFPV FC Gyroscope & Firmware Notes

Supplied by BETAFPV in the box with the flight controller. This applies to the
G473 AIO boards in this workshop, including the one in
[AIR65 F](/spec/air65-build/).

> [!CAUTION]
> **Do not flash official Betaflight firmware onto this board.** Betaflight has not
> released official firmware compatible with this gyroscope. The board ships with a
> customized build of the Betaflight *developer* firmware. Flashing a stock release
> can leave the gyro undetected and the craft unflyable. Watch for future support
> announcements before changing this.

---

## 1. Supported Gyroscopes

Because of the shortage of the ICM42688 chip, BETAFPV sourced alternative IMUs and
built a compatible firmware for them. Any given board may carry one of:

| Gyroscope | Notes |
| :--- | :--- |
| `ICM42688` | The original part, now in short supply |
| `ICM42622` | |
| `BMI270` | Fitted to AIR65 F, confirmed via `status` |
| `LSM6DSV16X` | |
| `LSM6DSK320X` | |

BETAFPV state that extensive testing confirms the substitutes meet their quality
standards.

To find out which one a given board actually has:

```bash
python tools/bf_cli.py "status"
```

Look for the `GYRO:` and `ACC:` lines.

---

## 2. Configurator

Because the firmware is a developer build, the release Betaflight Configurator may
refuse to connect or may show the wrong options. Use the development configurator
when adjusting parameters:

<https://master.app.betaflight.com/>

The Python tools in `tools/` talk to the board over plain serial and are unaffected
by this, so they work normally.

---

## 3. Missing or Blank OSD

If OSD information is missing or not displayed, set the display driver and video
standard explicitly:

```bash
python tools/bf_cli.py --save \
  "set osd_displayport_device = MAX7456" \
  "set vcd_video_system = NTSC"
```

Both of these are non-default values, so a fresh board or a restored backup can end
up on `AUTO` and show nothing. `AUTO` is the firmware default for each, which is
exactly the state BETAFPV are warning about.

> [!CAUTION]
> Do not "tidy" these two back to `AUTO` when copying an OSD layout between craft.
> This caught us once already on AIR65 F.
