# WhoopShop — AI Coding Agent Guidelines

Welcome to **WhoopShop**, a self-contained AI-assisted workshop environment for micro FPV drones (Tiny Whoops). 
These instructions apply to all AI Coding Agents (Google Antigravity, Claude Code, etc.) operating in this workspace.

---

## 1. Safety Protocols (CRITICAL)

> [!CAUTION]
> **PROPS OFF**: Before executing any command that touches motor settings, DShot protocols, arming flags, or motor testing, **always instruct the user to remove all propellers**.
> 
> **Bench Overheating & Battery Care**: 1S VTXs and AIO flight controllers heat up rapidly without flight airflow. Advise the user to use a bench cooling fan and disconnect batteries when performing long tuning sessions.
> 
> **Backup Before Save**: Before applying configuration changes (`set ...` + `--save`), always create a full CLI diff backup:
> ```bash
> python tools/backup_restore.py --backup
> ```

---

## 2. Local Workshop Site & Telemetry Capture (Zero External Dependencies)

WhoopShop includes a 100% pure Python local documentation website and an automated telemetry capturing tool. **No Hugo, Node, or extra binaries are required.**

- **Launch Local Website**: `python tools/serve_site.py` or `npm run dev` (serves at `http://localhost:8000/`).
- **Capture FC Telemetry into Log Entry**:
  ```bash
  python tools/capture_log.py --title "Hover & Noise Check" --log-file "btfl_001.bbl"
  ```
  This creates a formatted Markdown page under `content/log/YYYY-MM-DD-hover-noise-check.md` with captured FC status, arming flags, board targets, and Blackbox tables, which automatically renders on the local website!

---

## 3. Flight Controller Serial Communication Protocol

All serial interactions with the Flight Controller must use the provided Python tools in `tools/`. Do **not** write custom serial logic or rely on third-party MCP servers.

### Complete Tool Inventory
- **System Check**: `python tools/fc_check.py`
- **Pre-Flight Audit**: `python tools/preflight.py`
- **Execute CLI Commands**: `python tools/bf_cli.py "<cmd1>" "<cmd2>"`
- **Save CLI Changes**: `python tools/bf_cli.py --save "<set_cmd>"`
- **Read Live MSP Data / RC Channels**: `python tools/bf_msp.py [samples]`
- **Blackbox Log Helper**: `python tools/blackbox_tool.py`
- **PID & Rate Tuning Helper**: `python tools/tuning_tool.py`
- **ExpressLRS RX Helper**: `python tools/elrs_tool.py`
- **Motor & ESC Helper**: `python tools/motor_tool.py`
- **VTX & OSD Helper**: `python tools/vtx_osd_tool.py`
- **Backup & Restore Manager**: `python tools/backup_restore.py`
- **Telemetry & Log Capturer**: `python tools/capture_log.py`
- **Local Site Builder & Server**: `python tools/serve_site.py`

### CLI Entry & Exit Discipline
1. **Bare `#` Handshake**: Entering Betaflight CLI requires writing a bare `#` byte without a newline terminator (`\r\n`). Sending `#\r\n` causes the FC to stay silent. `tools/bf_cli.py` handles this automatically.
2. **Guaranteed Exit**: Every CLI session **must** end with `exit noreboot` (to return FC to normal/MSP state without rebooting) or `save` (reboots FC to write EEPROM). `tools/bf_cli.py` guarantees exit execution on completion or exception.
3. **Stuck in CLI Recovery**: If the board stops responding to CLI or MSP requests, it was likely left in CLI mode from an interrupted session. Unplug and replug the USB cable to reset the state machine.

---

## 4. Blackbox Log Management & Decoding

1. **Storage Location**: Raw `.bbl` recordings and decoded `.csv` / `.event` files belong in `logs/` (gitignored).
2. **Mass Storage Mode (`msc`)**:
   - Run `python tools/blackbox_tool.py --msc` to put the FC into USB mass-storage drive mode.
   - The device appears as a USB flash drive labelled `BETAFLT`.
   - Copy `btfl_*.bbl` files to `logs/`. Ignore `padding.txt` and `btfl_all.bbl`.
3. **Decoded Data Interpretation**:
   - `blackbox_sample_rate = 1/4` (default) logs 1 out of 4 loop iterations.
   - `blackbox_decode` will report *"75% of iterations are missing"*. This is **normal expected behavior** under 1/4 decimation, not data loss or corruption.
   - Motor Balance Metric: Compare mean `eRPM[n]` vs mean `motor[n]` across all 4 motors to check for motor degradation or cold solder joints.

---

## 5. Workshop Structure

- `content/`: Markdown pages for local site (`content/log/`, `content/spec/`, `content/docs/`, `content/reference/`).
- `skills/`: Antigravity skills (`betaflight`, `blackbox-analysis`, `elrs-config`, `motor-testing`, `preflight-check`, `serial-recovery`, `vtx-osd`).
- `tools/`: Cross-platform Python tools.
- `config/`: Baseline configuration templates and CLI backups (`config/backups/`).
- `workshop/`: `build_spec.md` (hardware inventory) and `flight_log.md` (test history & tuning journal).
- `logs/`: Local Blackbox log directory.
