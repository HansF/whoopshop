# WhoopShop Flight Log & Tuning Journal

Record flight tests, Blackbox analysis findings, PID/rate adjustments, and maintenance notes here.

---

## Flight Log Entry Template

### Flight Date: YYYY-MM-DD
- **Craft Name**: `WHOOP_SHOP_01`
- **Location / Setup**: Indoor Track / Living Room / Outdoor Park
- **Battery**: 1S 300mAh LiHV (Start: 4.35V | End: 3.50V)
- **Flight Duration**: 3m 15s
- **Blackbox Log File**: `btfl_001.bbl` (Source in `logs/`)

#### Flight Objectives
- [ ] Test baseline PID multipliers
- [ ] Verify motor balance across 4 corners
- [ ] Evaluate gyro noise floor FFT

#### Blackbox Analysis Findings
- **Sample Rate**: 1/4 decimation (~1 kHz effective log rate)
- **Motor Balance Ratios** (`mean eRPM / mean motor output` above idle):
  - Motor 1 (Rear Right) : `1.72`
  - Motor 2 (Front Right): `1.71`
  - Motor 3 (Rear Left)  : `1.73`
  - Motor 4 (Front Left) : `1.70`
  - *Status*: Balance within 2% spread — clean motor solder joints and healthy bearings.
- **Gyro Noise Floor**: Clean broadband response below 150 Hz; minor frame spike at 280 Hz handled by dynamic notch filter.

#### Adjustments Made
```bash
python tools/bf_cli.py --save "set p_pitch = 52" "set i_pitch = 85" "set d_pitch = 38"
```

#### Pilot Feedback
"P-term feels crisp. No oscillation on fast throttle punch-outs. Flight time solid."
