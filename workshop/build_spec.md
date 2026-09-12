# Tiny Whoop Hardware Spec & Build Sheet

Use this document to record the exact hardware configuration, component breakdown, and physical specs of your micro FPV drone.

---

## 1. Craft Overview

- **Craft Name**: `WHOOP_SHOP_01`
- **Airframe Type**: 65mm / 75mm / 85mm Micro Duct Frame
- **Class / Power**: 1S LiPo / LiHV (4.35V)
- **All-Up Weight (AUW)**: `0.0` g (with battery)
- **Dry Weight**: `0.0` g (without battery)

---

## 2. Hardware Component Inventory

| Component | Manufacturer & Model | Key Specifications / Firmware |
| :--- | :--- | :--- |
| **Frame** | *e.g. Meteor65 Pro 65mm* | 1.8g Polycarbonate |
| **Flight Controller** | *e.g. BETAFPV F4 1S 5A AIO* | STM32F411 / G473, Betaflight 4.5+ |
| **Motors** | *e.g. 0802 22000KV* | Unibell, 1.0mm shaft |
| **Propellers** | *e.g. Gemfan 31mm 3-Blade* | 1.0mm shaft hole |
| **ESC Firmware** | *e.g. Bluejay 0.20* | 48kHz PWM, DShot300 |
| **Receiver (RX)** | *e.g. Onboard Serial ELRS 2.4G* | ExpressLRS v3.x, Packet Rate 250Hz/500Hz |
| **Camera** | *e.g. C03 FPV Camera* | 1200TVL 1/3" CMOS |
| **Video Transmitter (VTX)** | *e.g. Onboard 25-400mW VTX* | SmartAudio / Tramp protocol |
| **Batteries** | *e.g. Lava 1S 300mAh 75C BT2.0* | LiHV 4.35V, BT2.0 Connector |

---

## 3. Physical Layout & Motor Order

- **Motor Direction**: Props Out / Props In (Default: Props Out recommended for duct efficiency)
- **ESC Protocol**: DShot300 with Bi-directional DShot enabled (`set dshot_bidir = ON`)
- **Motor Poles**: 12 (standard for 0802 / 0702 / 1102 micro brushless motors)
