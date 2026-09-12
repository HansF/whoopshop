# 🛸 WhoopShop — AI-Assisted Tiny Whoop FPV Workshop

Welcome to **WhoopShop**! This is a complete, self-contained starter template and toolkit for 1S/2S micro FPV drones (Tiny Whoops).

WhoopShop is built **agent-first**: you plug in your drone, launch your AI coding agent—such as **Google Antigravity** or **Claude Code / Cloud Code**—and let the agent handle connection testing, hardware diagnostics, CLI queries, Blackbox log extraction, and safe tuning for you.

---

## ⚠️ CRITICAL SAFETY DISCLAIMERS & WARNINGS

> [!CAUTION]
> ### 🚨 READ BEFORE CONNECTING YOUR DRONE
>
> 1. **INTERACTING OVER CLI CAN HAVE UNWANTED RESULTS**:
>    Executing Command Line Interface (CLI) commands directly modifies your Flight Controller's onboard EEPROM settings. **Incorrect CLI settings (e.g. wrong motor direction, inverted DShot protocols, altered arming flags, or incorrect PID gains) can cause unexpected motor arming, full-throttle flyaways, burnt ESCs, or total loss of craft control.** Always double-check commands before saving!
>
> 2. **ALWAYS REMOVE PROPELLERS (PROPS OFF ON BENCH)**:
>    Never plug in a battery or test motors while propellers are attached! Motors can spin unexpectedly at full speed during CLI configuration, testing, or firmware mode changes. **Always take off all 4 props before plugging in USB or battery on your workbench.**
>
> 3. **BENCH OVERHEATING**:
>    Micro FPV Video Transmitters (VTX) and All-In-One (AIO) flight controllers generate significant heat and rely on flight airflow to stay cool. **When connected on your bench, use a small USB fan to cool the board, or unplug the LiPo battery and power the FC via USB only.**
>
> 4. **ALWAYS BACK UP YOUR CONFIGURATION FIRST**:
>    Before making any changes, ask your AI agent to create a backup of your original working Betaflight configuration:
>    ```bash
>    python tools/backup_restore.py --backup
>    ```

---

## 🚀 Quickstart: Let Your AI Agent Handle Everything

WhoopShop is **100% self-contained in Python** and works on **Windows, macOS, and Linux**. You do **not** need to run complex setup commands or manually test connection ports—your AI agent does it for you.

### 1. Plug In Your Drone
Connect your Tiny Whoop flight controller to your computer using a USB cable (props off!). Make sure it is a data cable.

### 2. Open Workspace in Your AI Agent
Open this workspace folder in **Google Antigravity** or start **Claude Code**:

```bash
claude
```

### 3. Let Your Agent Connect & Inspect
Simply ask your AI agent:
> *"Connect to my drone and check hardware status."*

Your AI agent automatically reads `AGENT.md` and `skills/`, runs `python tools/fc_check.py` to auto-detect your Flight Controller serial port, verifies system tools, and reports connection status back to you!

---

## 💬 What You Can Ask Your AI Agent

Once connected, you can ask your agent to handle any workshop task in natural language:

- 🔍 **Diagnostics**: *"Check my FC status, CPU load, and arming disable flags."*
- 🛠️ **Tuning**: *"Preview the 65mm indoor tuning preset for my drone."*
- 📡 **Receiver Setup**: *"Check if my ExpressLRS receiver is set up with CRSF and AETR1234 channel map."*
- 📊 **Blackbox Extraction**: *"Put my drone into mass storage mode, copy my Blackbox logs, and analyze motor balance."*
- 📝 **Flight Logging**: *"Capture today's flight telemetry into a new flight log page."*
- 🌐 **Local Site**: *"Launch my local workshop website so I can view my logs in my browser."*

---

## 🛠️ Tool Cheat Sheet (For Reference)

Your AI agent uses these bundled Python tools automatically:

| Tool Script | What It Does | Handled by Agent |
| :--- | :--- | :--- |
| **`tools/fc_check.py`** | Scans USB ports and identifies connected Flight Controller. | ✅ Automatic |
| **`tools/bf_cli.py`** | Executes Betaflight CLI commands safely with bare `#` handshake and auto-exit. | ✅ Automatic |
| **`tools/bf_msp.py`** | Reads live telemetry and RC channel values (Roll, Pitch, Yaw, Throttle). | ✅ Automatic |
| **`tools/tuning_tool.py`** | Previews and applies curated PID & rate tuning presets for 65mm/75mm Whoops. | ✅ Automatic |
| **`tools/elrs_tool.py`** | Checks and configures ExpressLRS receiver settings (CRSF & channel mapping). | ✅ Automatic |
| **`tools/blackbox_tool.py`** | Reboots FC into USB Drive mode (`msc`) to copy and decode `.bbl` flight logs. | ✅ Automatic |
| **`tools/capture_log.py`** | Captures live FC telemetry into a published flight log Markdown entry. | ✅ Automatic |
| **`tools/preflight.py`** | Runs a multi-point arming, DShot, receiver, and flash audit before you fly. | ✅ Automatic |
| **`tools/motor_tool.py`** | Motor and ESC diagnostics, plus a props-off bench spin test. | ✅ Automatic |
| **`tools/vtx_osd_tool.py`** | Reads and sets video transmitter band, channel, power, and OSD elements. | ✅ Automatic |
| **`tools/backup_restore.py`** | Timestamped `diff all` backups and a full, verified restore. | ✅ Automatic |
| **`tools/analyze_log.py`** | Computes motor balance ratios and gyro noise floor from a decoded log. | ✅ Automatic |
| **`tools/dump_vars.py`** | Reads every setting your firmware exposes and regenerates the variable reference. | ✅ Automatic |
| **`tools/serve_site.py`** | Generates and serves your local workshop website at `http://localhost:8000/`, including the `/craft/` and `/tags/` collection pages. | ✅ Automatic |

---

## 📁 Workspace Folder Layout

```text
whoopshop/
├── AGENT.md                      # Universal instructions & safety rules for AI Coding Agents
├── CLAUDE.md                     # Quick guidelines for Claude Code / Cloud Code
├── README.md                     # Agent-first workspace manual & safety guide
├── requirements.txt              # Python requirements (pyserial)
├── package.json                  # Optional NPM script shortcuts
├── skills/                       # Google Antigravity Skills
│   ├── betaflight/
│   │   └── SKILL.md              # FC CLI & MSP interaction skill
│   ├── blackbox-analysis/
│   │   └── SKILL.md              # Blackbox extraction & log decoding skill
│   ├── elrs-config/
│   │   └── SKILL.md              # ExpressLRS receiver skill
│   └── serial-recovery/
│       └── SKILL.md              # Serial troubleshooting skill
├── tools/                        # 100% Pure-Python workshop tools
│   ├── fc_check.py               # Auto-detect connected FC across Windows/macOS/Linux
│   ├── bf_cli.py                 # Betaflight CLI runner (bare '#' prompt, safe exit)
│   ├── bf_msp.py                 # Pure Python MSP v1 reader (live RC channels & status)
│   ├── blackbox_tool.py          # Blackbox flash manager & log extractor
│   ├── capture_log.py            # FC telemetry & flight log markdown generator
│   ├── tuning_tool.py            # PID & rate tuning preset helper
│   ├── elrs_tool.py              # ExpressLRS receiver helper
│   └── serve_site.py             # Pure-Python zero-dependency site builder & server
├── content/                      # Your local website pages
│   ├── log/                      # Flight log entries
│   ├── spec/                     # Drone build specs
│   ├── docs/                     # Detailed FPV workshop guides
│   └── reference/                # CLI variable reference
├── config/                       # Baseline CLI diff templates
│   └── baseline_diff.txt         # Annotated 1S/2S micro quad baseline config
└── workshop/                     # User specs & flight log templates
    ├── build_spec.md             # Drone specs & component breakdown
    └── flight_log.md             # Flight logs & tuning journal
```

---

## 📄 License

[MIT License](LICENSE) — Free for all FPV pilots, makers, and developers!
