---
name: elrs-config
description: Configure ExpressLRS (ELRS) receiver settings, serial baud rates, channel mapping (AETR1234), packet rates, and telemetry output on Betaflight flight controllers.
---

# ExpressLRS (ELRS) Configuration Skill

Use this skill when verifying or configuring ExpressLRS receivers (SPI or Serial CRSF) connected to Tiny Whoop Flight Controllers.

---

## 1. Inspect Receiver Configuration

Run the ExpressLRS diagnostic tool:

```bash
python tools/elrs_tool.py --info
```

Or query CLI directly:

```bash
python tools/bf_cli.py "get serialrx_provider" "get serialrx_inverted" "get crsf_use_negotiated_baud" "map"
```

---

## 2. Recommended ELRS Settings for Micro Whoops

| Setting | Recommended Value | Reason |
| :--- | :--- | :--- |
| **Receiver Type** | Serial (via USART) or SPI | CRSF protocol support |
| **Serial RX Provider** | `CRSF` | Native ExpressLRS protocol |
| **Channel Map** | `AETR1234` | Standard Roll/Pitch/Yaw/Throttle order + AUX channels |
| **Packet Rate** | `250Hz` or `500Hz` | 250Hz provides optimal range/latency balance for 1S Whoops |
| **Telemetry Ratio** | `1:64` or `1:128` | Saves battery and airborne bandwidth while sending vbat data |

---

## 3. Apply ELRS Serial Receiver Preset

To set serial receiver protocol to CRSF and channel map to AETR1234:

```bash
python tools/elrs_tool.py --apply-crsf
```
