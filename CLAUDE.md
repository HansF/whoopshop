# WhoopShop — Working Notes for Claude Code

Self-contained cross-platform (Windows, Linux, macOS) workspace and AI toolkit for 1S/2S Tiny Whoop FPV micro-drones.

## Quick Reference Commands

- **Check FC Connection & Environment**: `python tools/fc_check.py`
- **Run Betaflight CLI Commands**: `python tools/bf_cli.py "status" "get osd_profile"`
- **Apply & Save Settings**: `python tools/bf_cli.py --save "set craft_name = WHOOP"`
- **Read Live Telemetry / RC**: `python tools/bf_msp.py --samples 5`
- **Manage Blackbox Flash**: `python tools/blackbox_tool.py --info`

## Architecture & Rules

1. **No External MCP Server**: We interact directly with the Flight Controller over USB serial via pure Python scripts (`tools/bf_cli.py`, `tools/bf_msp.py`).
2. **Cross-Platform First**: Python tools use `pyserial` port enumeration for Windows (`COM*`), macOS (`/dev/tty.usbmodem*`), and Linux (`/dev/ttyACM*`).
3. **CLI Exit Discipline**: Every CLI session must exit cleanly (`exit noreboot` or `save`). Failing to exit locks the FC in CLI mode, blocking MSP calls and subsequent CLI connections until USB is replugged.
4. **Never Flash Stock Betaflight**: The BETAFPV G473 boards run a *customized BETAFPV build of the Betaflight developer firmware*, because their gyro (BMI270 / ICM42622 / LSM6DSV16X and others substituted for the scarce ICM42688) is not supported by official releases. Flashing a stock release can leave the gyro undetected. Use the dev configurator at <https://master.app.betaflight.com/>. Keep `osd_displayport_device = MAX7456` and `vcd_video_system = NTSC` pinned or the OSD goes blank. See `content/reference/betafpv-fc-gyro-firmware-notes.md`.
5. **Blackbox Policy**: Raw `.bbl` and `.csv` files are saved in `logs/` (gitignored). Log pages in `workshop/flight_log.md` record analyzed metrics (motor ratios, gyro FFT noise floor).
