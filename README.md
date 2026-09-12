# 🛸 WhoopShop — AI-Assisted Tiny Whoop FPV Workshop

Welcome to **WhoopShop**! This is a complete, self-contained starter template and toolkit for 1S/2S micro FPV drones (Tiny Whoops). 

Whether you are a complete beginner or an experienced FPV pilot, WhoopShop lets you pair up with AI coding agents—such as **Google Antigravity** or **Claude Code / Cloud Code**—to tune your flight controller, analyze Blackbox logs, log test flights, and manage build specs cleanly over USB serial.

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
>    Before making any changes, save a backup of your original working Betaflight configuration:
>    ```bash
>    python tools/bf_cli.py "diff all" > config/my_original_backup.txt
>    ```

---

## 🚀 Beginner Quickstart: Get Up to Speed in 5 Minutes

You do **not** need to install Betaflight Configurator, Hugo, Node, or complex background servers. WhoopShop is **100% self-contained in Python** and works on **Windows, macOS, and Linux**.

### Step 1: Install Python Dependencies
Ensure you have Python 3 installed on your computer, open a terminal/command prompt in this folder, and run:

```bash
pip install -r requirements.txt
```
*(This installs `pyserial`, the only requirement needed to talk to your drone).*

### Step 2: Plug In Your Drone
Connect your Tiny Whoop flight controller to your computer using a USB cable. 
*(Make sure it is a **data cable**, not a power-only charging cable).*

### Step 3: Test Your Connection
Run the diagnostic scanner tool:

```bash
python tools/fc_check.py
```

If your drone is connected properly, you will see output like this:
```text
Found 1 Flight Controller candidate(s):
  [1] Device       : /dev/ttyACM0 (or COM3 on Windows)
      Description  : BETAFPVG473_V2
      Notes        : Flight Controller (VCP)
```

### Step 4: Start Your AI Agent
Open this workspace folder in **Google Antigravity** or start **Claude Code**:

```bash
claude
```

Your AI coding agent will automatically read `AGENT.md` and `skills/` to assist you safely! You can ask your agent questions like:
- *"Check my current Betaflight status and arming flags."*
- *"Help me tune my 65mm Whoop for smooth indoor flying."*
- *"Extract my Blackbox logs and check if my motors are balanced."*

### Step 5: Launch Your Local Workshop Website
View your personal flight logs and tuning documentation in a sleek web interface running locally on your machine:

```bash
python tools/serve_site.py
```
Open your browser to `http://localhost:8000/`. *(Press `Ctrl+C` in your terminal to stop the web server).*

---

## 🛠️ Tool Cheat Sheet (What Does Each Tool Do?)

| Tool Script | What It Does (Plain English) | How to Run It |
| :--- | :--- | :--- |
| **`tools/fc_check.py`** | Scans USB ports to detect your connected flight controller. | `python tools/fc_check.py` |
| **`tools/bf_cli.py`** | Sends safe Betaflight CLI commands without locking your drone's serial link. | `python tools/bf_cli.py "status"` |
| **`tools/bf_msp.py`** | Reads live telemetry and RC receiver channel values (Roll, Pitch, Yaw, Throttle). | `python tools/bf_msp.py --samples 5` |
| **`tools/tuning_tool.py`** | Previews or applies curated PID & rate tuning presets for 65mm/75mm Whoops. | `python tools/tuning_tool.py --list` |
| **`tools/elrs_tool.py`** | Checks and configures ExpressLRS receiver settings (CRSF & channel mapping). | `python tools/elrs_tool.py --info` |
| **`tools/blackbox_tool.py`** | Reboots FC into USB Drive mode (`msc`) to copy and decode `.bbl` flight logs. | `python tools/blackbox_tool.py --info` |
| **`tools/capture_log.py`** | Automatically captures live FC telemetry into a published flight log entry. | `python tools/capture_log.py --title "First Flight"` |
| **`tools/serve_site.py`** | Generates and serves your local workshop website at `http://localhost:8000/`. | `python tools/serve_site.py` |

---

## 📁 Workspace Folder Layout

```text
whoopshop/
├── AGENT.md                      # Universal instructions & safety rules for AI Coding Agents
├── CLAUDE.md                     # Quick guidelines for Claude Code / Cloud Code
├── README.md                     # This manual & beginner safety guide
├── requirements.txt              # Python requirements (pyserial)
├── package.json                  # Optional NPM script shortcuts (npm run dev, npm run check, etc.)
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
