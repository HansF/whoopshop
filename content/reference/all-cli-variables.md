---
title: "Complete CLI Variable Reference"
draft: false
tags: [cli, reference]
---

Every setting exposed by `Betaflight / STM32G47X (G473) 2026.6.0-alpha Apr 15 2026 / 16:24:57 (norevision) MSP API: 1.48`.

Generated from a connected flight controller with `python tools/dump_vars.py`. Regenerate it after a firmware update, or to match a different board.

**561 variables.** A variable marked with a profile is stored per profile, so switching profiles changes its value.

| Variable | Type | Allowed | Profile |
| :--- | :--- | :--- | :--- |
| `3d_deadband_high` | int | 1500 to 2250 |  |
| `3d_deadband_low` | int | 750 to 1500 |  |
| `3d_deadband_throttle` | int | 1 to 100 |  |
| `3d_limit_high` | int | 1500 to 2250 |  |
| `3d_limit_low` | int | 750 to 1500 |  |
| `3d_neutral` | int | 750 to 2250 |  |
| `3d_switched_mode` | enum | `OFF`, `ON` |  |
| `abs_control_cutoff` | int | 1 to 45 | PID profile |
| `abs_control_error_limit` | int | 1 to 45 | PID profile |
| `abs_control_gain` | int | 0 to 20 | PID profile |
| `abs_control_limit` | int | 10 to 255 | PID profile |
| `acc_calibration` | array | array |  |
| `acc_hardware` | enum | `AUTO`, `NONE`, `MPU6050`, `MPU6000`, `MPU6500`, `MPU9250`, `ICM20601`, `ICM20602`, `ICM20608G`, `ICM20649`, `ICM20689`, `ICM42605`, `ICM42688P`, `BMI160`, `BMI270`, `LSM6DSO`, `LSM6DSV16X`, `IIM42653`, `ICM45605`, `ICM45686`, `ICM40609D`, `IIM42652`, `LSM6DSK320X`, `ICM42622P`, `ICM42686P`, `VIRTUAL` |  |
| `acc_limit` | int | 0 to 500 | PID profile |
| `acc_limit_yaw` | int | 0 to 500 | PID profile |
| `acc_lpf_hz` | int | 0 to 500 |  |
| `acc_trim_pitch` | int | -300 to 300 |  |
| `acc_trim_roll` | int | -300 to 300 |  |
| `adc_device` | int | 0 to 5 |  |
| `adc_tempsensor_calibration110` | int | 0 to 2000 |  |
| `adc_tempsensor_calibration30` | int | 0 to 2000 |  |
| `adc_vrefint_calibration` | int | 0 to 2000 |  |
| `airmode_start_throttle_percent` | int | 0 to 100 |  |
| `align_board_pitch` | int | -180 to 360 |  |
| `align_board_roll` | int | -180 to 360 |  |
| `align_board_yaw` | int | -180 to 360 |  |
| `altitude_d_lpf` | int | 10 to 1000 |  |
| `altitude_lpf` | int | 10 to 1000 |  |
| `altitude_prefer_baro` | int | 0 to 100 |  |
| `altitude_source` | enum | `DEFAULT`, `BARO_ONLY`, `GPS_ONLY`, `RANGEFINDER_PREFER`, `RANGEFINDER_ONLY` |  |
| `angle_earth_ref` | int | 0 to 100 | PID profile |
| `angle_feedforward` | int | 0 to 200 | PID profile |
| `angle_feedforward_smoothing_ms` | int | 10 to 250 | PID profile |
| `angle_limit` | int | 10 to 80 | PID profile |
| `angle_p_gain` | int | 0 to 200 | PID profile |
| `anti_gravity_cutoff_hz` | int | 2 to 50 | PID profile |
| `anti_gravity_gain` | int | 0 to 250 | PID profile |
| `anti_gravity_p_gain` | int | 0 to 250 | PID profile |
| `ap_altitude_d` | int | 0 to 200 |  |
| `ap_altitude_f` | int | 0 to 200 |  |
| `ap_altitude_i` | int | 0 to 200 |  |
| `ap_altitude_p` | int | 0 to 200 |  |
| `ap_hover_throttle` | int | 0 to 1700 |  |
| `ap_landing_altitude_m` | int | 0 to 200 |  |
| `ap_max_angle` | int | 10 to 70 |  |
| `ap_max_velocity` | int | 100 to 5000 |  |
| `ap_position_a` | int | 0 to 200 |  |
| `ap_position_cutoff` | int | 10 to 250 |  |
| `ap_position_d` | int | 0 to 200 |  |
| `ap_position_i` | int | 0 to 200 |  |
| `ap_position_ii` | int | 0 to 200 |  |
| `ap_position_p` | int | 0 to 200 |  |
| `ap_throttle_max` | int | 1400 to 2000 |  |
| `ap_throttle_min` | int | 1050 to 1400 |  |
| `ap_velocity_control_enable` | enum | `OFF`, `ON` |  |
| `ap_velocity_d` | int | 0 to 100 |  |
| `ap_velocity_drag_coeff` | int | 0 to 1000 |  |
| `ap_velocity_i` | int | 0 to 200 |  |
| `ap_velocity_p` | int | 0 to 200 |  |
| `auto_disarm_delay` | int | 0 to 60 |  |
| `auto_profile_cell_count` | int | -1 to 8 | PID profile |
| `bat_capacity` | int | 0 to 20000 | battery profile |
| `battery_meter` | enum | `NONE`, `ADC`, `ESC` |  |
| `battery_profile_name` | string | 1 to 8 characters | battery profile |
| `beeper_dshot_beacon_tone` | int | 1 to 5 |  |
| `beeper_frequency` | int | 0 to 16000 |  |
| `beeper_inversion` | enum | `OFF`, `ON` |  |
| `beeper_od` | enum | `OFF`, `ON` |  |
| `blackbox_device` | enum | `NONE`, `SPIFLASH`, `SDCARD`, `SERIAL` |  |
| `blackbox_disable_acc` | enum | `OFF`, `ON` |  |
| `blackbox_disable_attitude` | enum | `OFF`, `ON` |  |
| `blackbox_disable_bat` | enum | `OFF`, `ON` |  |
| `blackbox_disable_debug` | enum | `OFF`, `ON` |  |
| `blackbox_disable_gyro` | enum | `OFF`, `ON` |  |
| `blackbox_disable_gyrounfilt` | enum | `OFF`, `ON` |  |
| `blackbox_disable_motors` | enum | `OFF`, `ON` |  |
| `blackbox_disable_pids` | enum | `OFF`, `ON` |  |
| `blackbox_disable_rc` | enum | `OFF`, `ON` |  |
| `blackbox_disable_rpm` | enum | `OFF`, `ON` |  |
| `blackbox_disable_rssi` | enum | `OFF`, `ON` |  |
| `blackbox_disable_servos` | enum | `OFF`, `ON` |  |
| `blackbox_disable_setpoint` | enum | `OFF`, `ON` |  |
| `blackbox_high_resolution` | enum | `OFF`, `ON` |  |
| `blackbox_mode` | enum | `NORMAL`, `MOTOR_TEST`, `ALWAYS` |  |
| `blackbox_sample_rate` | enum | `1/1`, `1/2`, `1/4`, `1/8`, `1/16` |  |
| `box_user_1_name` | string | 1 to 16 characters |  |
| `box_user_2_name` | string | 1 to 16 characters |  |
| `box_user_3_name` | string | 1 to 16 characters |  |
| `box_user_4_name` | string | 1 to 16 characters |  |
| `cbat_alert_percent` | int | 0 to 100 | battery profile |
| `channel_forwarding_start` | int | 4 to 18 |  |
| `cpu_late_limit_permille` | int | 0 to 100 |  |
| `cpu_overclock` | enum | `OFF`, `192MHZ`, `216MHZ`, `240MHZ` |  |
| `craft_name` | string | 1 to 16 characters |  |
| `crash_delay` | int | 0 to 500 | PID profile |
| `crash_dthreshold` | int | 10 to 2000 | PID profile |
| `crash_gthreshold` | int | 100 to 2000 | PID profile |
| `crash_limit_yaw` | int | 0 to 1000 | PID profile |
| `crash_recovery` | enum | `OFF`, `ON`, `BEEP`, `DISARM` | PID profile |
| `crash_recovery_angle` | int | 5 to 30 | PID profile |
| `crash_recovery_rate` | int | 50 to 255 | PID profile |
| `crash_setpoint_threshold` | int | 50 to 2000 | PID profile |
| `crash_time` | int | 100 to 5000 | PID profile |
| `crashflip_auto_rearm` | enum | `OFF`, `ON` |  |
| `crashflip_motor_percent` | int | 0 to 100 |  |
| `crashflip_rate` | int | 0 to 250 |  |
| `crsf_tlm_accgyro` | enum | `OFF`, `ON` |  |
| `crsf_use_negotiated_baud` | enum | `OFF`, `ON` |  |
| `current_meter` | enum | `NONE`, `ADC`, `VIRTUAL`, `ESC`, `MSP` |  |
| `d_max_advance` | int | 0 to 200 | PID profile |
| `d_max_gain` | int | 0 to 100 | PID profile |
| `d_max_pitch` | int | 0 to 250 | PID profile |
| `d_max_roll` | int | 0 to 250 | PID profile |
| `d_max_yaw` | int | 0 to 250 | PID profile |
| `d_pitch` | int | 0 to 250 | PID profile |
| `d_roll` | int | 0 to 250 | PID profile |
| `d_yaw` | int | 0 to 250 | PID profile |
| `deadband` | int | 0 to 32 |  |
| `debug_mode` | enum | `NONE`, `CYCLETIME`, `BATTERY`, `GYRO_FILTERED`, `ACCELEROMETER`, `PIDLOOP`, `RC_INTERPOLATION`, `ANGLERATE`, `ESC_SENSOR`, `SCHEDULER`, `STACK`, `ESC_SENSOR_RPM`, `ESC_SENSOR_TMP`, `ALTITUDE`, `FFT`, `FFT_TIME`, `FFT_FREQ`, `RX_FRSKY_SPI`, `RX_SFHSS_SPI`, `GYRO_RAW`, `MULTI_GYRO_RAW`, `MULTI_GYRO_DIFF`, `MAX7456_SIGNAL`, `MAX7456_SPICLOCK`, `SBUS`, `FPORT`, `RANGEFINDER`, `RANGEFINDER_QUALITY`, `OPTICALFLOW`, `LIDAR_TF`, `ADC_INTERNAL`, `RUNAWAY_TAKEOFF`, `SDIO`, `CURRENT_SENSOR`, `USB`, `SMARTAUDIO`, `RTH`, `ITERM_RELAX`, `ACRO_TRAINER`, `RC_SMOOTHING`, `RX_SIGNAL_LOSS`, `RC_SMOOTHING_RATE`, `ANTI_GRAVITY`, `DYN_LPF`, `RX_SPEKTRUM_SPI`, `DSHOT_RPM_TELEMETRY`, `RPM_FILTER`, `D_MAX`, `AC_CORRECTION`, `AC_ERROR`, `MULTI_GYRO_SCALED`, `DSHOT_RPM_ERRORS`, `CRSF_LINK_STATISTICS_UPLINK`, `CRSF_LINK_STATISTICS_PWR`, `CRSF_LINK_STATISTICS_DOWN`, `BARO`, `AUTOPILOT_ALTITUDE`, `DYN_IDLE`, `FEEDFORWARD_LIMIT`, `FEEDFORWARD`, `BLACKBOX_OUTPUT`, `GYRO_SAMPLE`, `RX_TIMING`, `D_LPF`, `VTX_TRAMP`, `GHST`, `GHST_MSP`, `SCHEDULER_DETERMINISM`, `TIMING_ACCURACY`, `RX_EXPRESSLRS_SPI`, `RX_EXPRESSLRS_PHASELOCK`, `RX_STATE_TIME`, `GPS_RESCUE_VELOCITY`, `GPS_RESCUE_HEADING`, `GPS_RESCUE_TRACKING`, `GPS_CONNECTION`, `ATTITUDE`, `VTX_MSP`, `GPS_DOP`, `FAILSAFE`, `GYRO_CALIBRATION`, `ANGLE_MODE`, `ANGLE_TARGET`, `CURRENT_ANGLE`, `DSHOT_TELEMETRY_COUNTS`, `RPM_LIMIT`, `RC_STATS`, `MAG_CALIB`, `MAG_TASK_RATE`, `EZLANDING`, `TPA`, `S_TERM`, `SPA`, `TASK`, `GIMBAL`, `WING_SETPOINT`, `AUTOPILOT_POSITION`, `CHIRP`, `FLASH_TEST_PRBS`, `MAVLINK_TELEMETRY`, `AUTOPILOT_PID` |  |
| `displayport_max7456_blk` | int | 0 to 3 |  |
| `displayport_max7456_col_adjust` | int | -6 to 0 |  |
| `displayport_max7456_inv` | enum | `OFF`, `ON` |  |
| `displayport_max7456_row_adjust` | int | -3 to 0 |  |
| `displayport_max7456_wht` | int | 0 to 3 |  |
| `displayport_msp_col_adjust` | int | -6 to 0 |  |
| `displayport_msp_fonts` | array | array |  |
| `displayport_msp_row_adjust` | int | -3 to 0 |  |
| `displayport_msp_use_device_blink` | enum | `OFF`, `ON` |  |
| `dshot_bidir` | enum | `OFF`, `ON` |  |
| `dshot_bitbang` | enum | `OFF`, `ON`, `AUTO` |  |
| `dshot_bitbang_timer` | enum | `AUTO`, `TIM1`, `TIM8` |  |
| `dshot_burst` | enum | `OFF`, `ON`, `AUTO` |  |
| `dshot_edt` | enum | `OFF`, `ON`, `FORCE` |  |
| `dterm_lpf1_dyn_expo` | int | 0 to 10 | PID profile |
| `dterm_lpf1_dyn_max_hz` | int | 0 to 1000 | PID profile |
| `dterm_lpf1_dyn_min_hz` | int | 0 to 1000 | PID profile |
| `dterm_lpf1_static_hz` | int | 0 to 1000 | PID profile |
| `dterm_lpf1_type` | enum | `PT1`, `BIQUAD`, `PT2`, `PT3` | PID profile |
| `dterm_lpf2_static_hz` | int | 0 to 1000 | PID profile |
| `dterm_lpf2_type` | enum | `PT1`, `BIQUAD`, `PT2`, `PT3` | PID profile |
| `dterm_notch_cutoff` | int | 0 to 1000 | PID profile |
| `dterm_notch_hz` | int | 0 to 1000 | PID profile |
| `dyn_idle_d_gain` | int | 0 to 250 | PID profile |
| `dyn_idle_i_gain` | int | 1 to 250 | PID profile |
| `dyn_idle_max_increase` | int | 10 to 255 | PID profile |
| `dyn_idle_min_rpm` | int | 0 to 200 | PID profile |
| `dyn_idle_p_gain` | int | 1 to 250 | PID profile |
| `dyn_notch_count` | int | 0 to 7 |  |
| `dyn_notch_max_hz` | int | 200 to 1000 |  |
| `dyn_notch_min_hz` | int | 20 to 250 |  |
| `dyn_notch_q` | int | 1 to 1000 |  |
| `enable_stick_arming` | enum | `OFF`, `ON` |  |
| `esc_sensor_current_offset` | int | 0 to 16000 |  |
| `esc_sensor_halfduplex` | enum | `OFF`, `ON` |  |
| `ez_landing_limit` | int | 0 to 75 | PID profile |
| `ez_landing_speed` | int | 0 to 250 | PID profile |
| `ez_landing_threshold` | int | 0 to 200 | PID profile |
| `f_pitch` | int | 0 to 1000 | PID profile |
| `f_roll` | int | 0 to 1000 | PID profile |
| `f_yaw` | int | 0 to 1000 | PID profile |
| `failsafe_delay` | int | 1 to 200 |  |
| `failsafe_landing_time` | int | 0 to 250 |  |
| `failsafe_procedure` | enum | `AUTO-LAND`, `DROP`, `GPS-RESCUE` |  |
| `failsafe_recovery_delay` | int | 1 to 200 |  |
| `failsafe_stick_threshold` | int | 0 to 50 |  |
| `failsafe_switch_mode` | enum | `STAGE1`, `KILL`, `STAGE2` |  |
| `failsafe_throttle` | int | 750 to 2250 |  |
| `failsafe_throttle_low_delay` | int | 0 to 300 |  |
| `feedforward_averaging` | enum | `OFF`, `2_POINT`, `3_POINT`, `4_POINT` | PID profile |
| `feedforward_boost` | int | 0 to 50 | PID profile |
| `feedforward_jitter_factor` | int | 0 to 20 | PID profile |
| `feedforward_max_rate_limit` | int | 0 to 200 | PID profile |
| `feedforward_smooth_factor` | int | 0 to 95 | PID profile |
| `feedforward_transition` | int | 0 to 100 | PID profile |
| `feedforward_yaw_hold_gain` | int | 0 to 100 | PID profile |
| `feedforward_yaw_hold_time` | int | 10 to 250 | PID profile |
| `flash_spi_bus` | int | 0 to 4 |  |
| `force_battery_cell_count` | int | 0 to 24 | battery profile |
| `fpv_mix_degrees` | int | 0 to 90 |  |
| `frsky_vfas_precision` | int | 0 to 1 |  |
| `gimbal_mode` | enum | `NORMAL`, `MIXTILT` |  |
| `gyro_1_bustype` | enum | `NONE`, `I2C`, `SPI`, `SLAVE` |  |
| `gyro_1_i2c_address` | int | 0 to 119 |  |
| `gyro_1_spibus` | int | 0 to 4 |  |
| `gyro_cal_on_first_arm` | enum | `OFF`, `ON` |  |
| `gyro_calib_duration` | int | 50 to 3000 |  |
| `gyro_calib_noise_limit` | int | 0 to 200 |  |
| `gyro_filter_debug_axis` | enum | `ROLL`, `PITCH`, `YAW` |  |
| `gyro_hardware_lpf` | enum | `NORMAL`, `OPTION_1`, `OPTION_2`, `EXPERIMENTAL` |  |
| `gyro_lpf1_dyn_expo` | int | 0 to 10 |  |
| `gyro_lpf1_dyn_max_hz` | int | 0 to 1000 |  |
| `gyro_lpf1_dyn_min_hz` | int | 0 to 1000 |  |
| `gyro_lpf1_static_hz` | int | 0 to 1000 |  |
| `gyro_lpf1_type` | enum | `PT1`, `BIQUAD`, `PT2`, `PT3` |  |
| `gyro_lpf2_static_hz` | int | 0 to 1000 |  |
| `gyro_lpf2_type` | enum | `PT1`, `BIQUAD`, `PT2`, `PT3` |  |
| `gyro_notch1_cutoff` | int | 0 to 1000 |  |
| `gyro_notch1_hz` | int | 0 to 1000 |  |
| `gyro_notch2_cutoff` | int | 0 to 1000 |  |
| `gyro_notch2_hz` | int | 0 to 1000 |  |
| `gyro_offset_yaw` | int | -1000 to 1000 |  |
| `gyro_overflow_detect` | enum | `OFF`, `YAW`, `ALL` |  |
| `horizon_delay_ms` | int | 10 to 5000 | PID profile |
| `horizon_ignore_sticks` | enum | `OFF`, `ON` | PID profile |
| `horizon_level_strength` | int | 0 to 100 | PID profile |
| `horizon_limit_degrees` | int | 10 to 250 | PID profile |
| `horizon_limit_sticks` | int | 10 to 200 | PID profile |
| `hott_alarm_int` | int | 0 to 120 |  |
| `i2c1_clockspeed_khz` | int | 100 to 1300 |  |
| `i2c1_pullup` | enum | `OFF`, `ON` |  |
| `i2c2_clockspeed_khz` | int | 100 to 1300 |  |
| `i2c2_pullup` | enum | `OFF`, `ON` |  |
| `i2c3_clockspeed_khz` | int | 100 to 1300 |  |
| `i2c3_pullup` | enum | `OFF`, `ON` |  |
| `i2c4_clockspeed_khz` | int | 100 to 1300 |  |
| `i2c4_pullup` | enum | `OFF`, `ON` |  |
| `i_pitch` | int | 0 to 250 | PID profile |
| `i_roll` | int | 0 to 250 | PID profile |
| `i_yaw` | int | 0 to 250 | PID profile |
| `ibat_lpf_period` | int | 0 to 255 |  |
| `ibata_offset` | int | -32000 to 32000 |  |
| `ibata_scale` | int | -16000 to 16000 |  |
| `ibatv_offset` | int | 0 to 16000 |  |
| `ibatv_scale` | int | -16000 to 16000 |  |
| `imu_dcm_ki` | int | 0 to 32000 |  |
| `imu_dcm_kp` | int | 0 to 32000 |  |
| `imu_process_denom` | int | 1 to 4 |  |
| `input_filtering_mode` | enum | `OFF`, `ON` |  |
| `integrated_yaw_relax` | int | 0 to 255 | PID profile |
| `iterm_relax` | enum | `OFF`, `RP`, `RPY`, `RP_INC`, `RPY_INC` | PID profile |
| `iterm_relax_cutoff` | int | 1 to 50 | PID profile |
| `iterm_relax_type` | enum | `GYRO`, `SETPOINT` | PID profile |
| `iterm_rotation` | enum | `OFF`, `ON` | PID profile |
| `iterm_windup` | int | 20 to 100 | PID profile |
| `landing_disarm_threshold` | int | 0 to 250 | PID profile |
| `launch_angle_limit` | int | 0 to 80 | PID profile |
| `launch_control_gain` | int | 0 to 200 | PID profile |
| `launch_control_mode` | enum | `NORMAL`, `PITCHONLY`, `FULL` | PID profile |
| `launch_trigger_allow_reset` | enum | `OFF`, `ON` | PID profile |
| `launch_trigger_throttle_percent` | int | 0 to 90 | PID profile |
| `led_inversion` | int | 0 to 7 |  |
| `level_race_mode` | enum | `OFF`, `ON` | PID profile |
| `max7456_clock` | enum | `HALF`, `NOMINAL`, `DOUBLE` |  |
| `max7456_preinit_opu` | enum | `OFF`, `ON` |  |
| `max7456_spi_bus` | int | 0 to 4 |  |
| `max_aux_channels` | int | 0 to 14 |  |
| `max_check` | int | 750 to 2250 |  |
| `max_throttle` | int | 750 to 2250 |  |
| `mco_divider` | int | 0 to 4 |  |
| `mco_on_pa8` | enum | `OFF`, `ON` |  |
| `mco_source` | int | 0 to 7 |  |
| `mid_rc` | int | 1200 to 1700 |  |
| `min_check` | int | 750 to 2250 |  |
| `min_command` | int | 750 to 2250 |  |
| `mixer_type` | enum | `LEGACY`, `LINEAR`, `DYNAMIC`, `EZLANDING` |  |
| `motor_idle` | int | 0 to 2000 |  |
| `motor_kv` | int | 1 to 40000 |  |
| `motor_output_limit` | int | 1 to 100 | PID profile |
| `motor_output_reordering` | array | array |  |
| `motor_poles` | int | 4 to 255 |  |
| `motor_pwm_inversion` | enum | `OFF`, `ON` |  |
| `motor_pwm_protocol` | enum | `PWM`, `ONESHOT125`, `ONESHOT42`, `MULTISHOT`, `BRUSHED`, `DSHOT150`, `DSHOT300`, `DSHOT600`, `PROSHOT1000`, `DISABLED` |  |
| `motor_pwm_rate` | int | 200 to 32000 |  |
| `msp_override_channels_mask` | int | 0 to 262143 |  |
| `msp_override_failsafe` | enum | `OFF`, `ON` |  |
| `osd_adjustment_range_pos` | int | 0 to 65535 |  |
| `osd_ah_invert` | enum | `OFF`, `ON` |  |
| `osd_ah_max_pit` | int | 0 to 90 |  |
| `osd_ah_max_rol` | int | 0 to 90 |  |
| `osd_ah_pos` | int | 0 to 65535 |  |
| `osd_ah_sbar_pos` | int | 0 to 65535 |  |
| `osd_alt_alarm` | int | 0 to 10000 |  |
| `osd_altitude_pos` | int | 0 to 65535 |  |
| `osd_anti_gravity_pos` | int | 0 to 65535 |  |
| `osd_arming_logo` | int | 0 to 3 |  |
| `osd_aux_channel` | int | 1 to 18 |  |
| `osd_aux_pos` | int | 0 to 65535 |  |
| `osd_aux_scale` | int | 1 to 1000 |  |
| `osd_aux_symbol` | int | 0 to 255 |  |
| `osd_avg_cell_voltage_pos` | int | 0 to 65535 |  |
| `osd_battery_profile_name_pos` | int | 0 to 65535 |  |
| `osd_battery_usage_pos` | int | 0 to 65535 |  |
| `osd_camera_frame_height` | int | 2 to 16 |  |
| `osd_camera_frame_pos` | int | 0 to 65535 |  |
| `osd_camera_frame_width` | int | 2 to 30 |  |
| `osd_cap_alarm` | int | 0 to 20000 |  |
| `osd_compass_bar_pos` | int | 0 to 65535 |  |
| `osd_core_temp_alarm` | int | 0 to 255 |  |
| `osd_core_temp_pos` | int | 0 to 65535 |  |
| `osd_craft_name_pos` | int | 0 to 65535 |  |
| `osd_craftname_msgs` | enum | `OFF`, `ON` |  |
| `osd_crosshairs_pos` | int | 0 to 65535 |  |
| `osd_current_pos` | int | 0 to 65535 |  |
| `osd_custom_serial_text_pos` | int | 0 to 65535 |  |
| `osd_custom_serial_text_terminator` | enum | `NULL`, `LF` |  |
| `osd_debug2_pos` | int | 0 to 65535 |  |
| `osd_debug_pos` | int | 0 to 65535 |  |
| `osd_disarmed_pos` | int | 0 to 65535 |  |
| `osd_displayport_device` | enum | `NONE`, `AUTO`, `MAX7456`, `MSP`, `FRSKYOSD` |  |
| `osd_distance_alarm` | int | 0 to 65535 |  |
| `osd_efficiency_pos` | int | 0 to 65535 |  |
| `osd_esc_current_alarm` | int | -1 to 32767 |  |
| `osd_esc_rpm_alarm` | int | -1 to 32767 |  |
| `osd_esc_rpm_freq_pos` | int | 0 to 65535 |  |
| `osd_esc_rpm_pos` | int | 0 to 65535 |  |
| `osd_esc_temp_alarm` | int | 0 to 255 |  |
| `osd_esc_tmp_pos` | int | 0 to 65535 |  |
| `osd_flight_dist_pos` | int | 0 to 65535 |  |
| `osd_flip_arrow_pos` | int | 0 to 65535 |  |
| `osd_flymode_pos` | int | 0 to 65535 |  |
| `osd_framerate_hz` | int | 1 to 60 |  |
| `osd_g_force_pos` | int | 0 to 65535 |  |
| `osd_gps_lat_pos` | int | 0 to 65535 |  |
| `osd_gps_lon_pos` | int | 0 to 65535 |  |
| `osd_gps_sats_pos` | int | 0 to 65535 |  |
| `osd_gps_sats_show_pdop` | enum | `OFF`, `ON` |  |
| `osd_gps_speed_pos` | int | 0 to 65535 |  |
| `osd_home_dir_pos` | int | 0 to 65535 |  |
| `osd_home_dist_pos` | int | 0 to 65535 |  |
| `osd_link_quality_alarm` | int | 0 to 100 |  |
| `osd_link_quality_pos` | int | 0 to 65535 |  |
| `osd_link_tx_power_pos` | int | 0 to 65535 |  |
| `osd_log_status_pos` | int | 0 to 65535 |  |
| `osd_logo_on_arming` | enum | `OFF`, `ON`, `FIRST_ARMING` |  |
| `osd_logo_on_arming_duration` | int | 5 to 50 |  |
| `osd_mah_drawn_pos` | int | 0 to 65535 |  |
| `osd_menu_background` | enum | `TRANSPARENT`, `BLACK`, `GRAY`, `LIGHT_GRAY` |  |
| `osd_motor_diag_pos` | int | 0 to 65535 |  |
| `osd_nheading_pos` | int | 0 to 65535 |  |
| `osd_pid_pitch_pos` | int | 0 to 65535 |  |
| `osd_pid_profile_name_pos` | int | 0 to 65535 |  |
| `osd_pid_roll_pos` | int | 0 to 65535 |  |
| `osd_pid_yaw_pos` | int | 0 to 65535 |  |
| `osd_pidrate_profile_pos` | int | 0 to 65535 |  |
| `osd_pilot_name_pos` | int | 0 to 65535 |  |
| `osd_pit_ang_pos` | int | 0 to 65535 |  |
| `osd_power_pos` | int | 0 to 65535 |  |
| `osd_profile` | int | 1 to 3 |  |
| `osd_profile_1_name` | string | 1 to 16 characters |  |
| `osd_profile_2_name` | string | 1 to 16 characters |  |
| `osd_profile_3_name` | string | 1 to 16 characters |  |
| `osd_profile_name_pos` | int | 0 to 65535 |  |
| `osd_rate_profile_name_pos` | int | 0 to 65535 |  |
| `osd_rcchannels` | array | array |  |
| `osd_rcchannels_pos` | int | 0 to 65535 |  |
| `osd_ready_mode_pos` | int | 0 to 65535 |  |
| `osd_remaining_time_estimate_pos` | int | 0 to 65535 |  |
| `osd_rol_ang_pos` | int | 0 to 65535 |  |
| `osd_rsnr_alarm` | int | -30 to 20 |  |
| `osd_rsnr_pos` | int | 0 to 65535 |  |
| `osd_rssi_alarm` | int | 0 to 100 |  |
| `osd_rssi_dbm_alarm` | int | -130 to 0 |  |
| `osd_rssi_dbm_pos` | int | 0 to 65535 |  |
| `osd_rssi_pos` | int | 0 to 65535 |  |
| `osd_rtc_date_time_pos` | int | 0 to 65535 |  |
| `osd_stat_avg_cell_value` | enum | `OFF`, `ON` |  |
| `osd_stat_bitmask` | int | 0 to 4294967295 |  |
| `osd_stick_overlay_left_pos` | int | 0 to 65535 |  |
| `osd_stick_overlay_radio_mode` | int | 1 to 4 |  |
| `osd_stick_overlay_right_pos` | int | 0 to 65535 |  |
| `osd_sys_bitrate_pos` | int | 0 to 65535 |  |
| `osd_sys_delay_pos` | int | 0 to 65535 |  |
| `osd_sys_distance_pos` | int | 0 to 65535 |  |
| `osd_sys_fan_speed_pos` | int | 0 to 65535 |  |
| `osd_sys_goggle_dvr_pos` | int | 0 to 65535 |  |
| `osd_sys_goggle_voltage_pos` | int | 0 to 65535 |  |
| `osd_sys_lq_pos` | int | 0 to 65535 |  |
| `osd_sys_vtx_dvr_pos` | int | 0 to 65535 |  |
| `osd_sys_vtx_temp_pos` | int | 0 to 65535 |  |
| `osd_sys_vtx_voltage_pos` | int | 0 to 65535 |  |
| `osd_sys_warnings_pos` | int | 0 to 65535 |  |
| `osd_throttle_pos` | int | 0 to 65535 |  |
| `osd_tim1` | int | 0 to 32767 |  |
| `osd_tim2` | int | 0 to 32767 |  |
| `osd_tim_1_pos` | int | 0 to 65535 |  |
| `osd_tim_2_pos` | int | 0 to 65535 |  |
| `osd_total_flights_pos` | int | 0 to 65535 |  |
| `osd_units` | enum | `IMPERIAL`, `METRIC`, `BRITISH` |  |
| `osd_up_down_reference_pos` | int | 0 to 65535 |  |
| `osd_vbat_pos` | int | 0 to 65535 |  |
| `osd_vtx_channel_pos` | int | 0 to 65535 |  |
| `osd_warn_bitmask` | int | 0 to 4294967295 |  |
| `osd_warnings_pos` | int | 0 to 65535 |  |
| `osd_wh_drawn_pos` | int | 0 to 65535 |  |
| `p_pitch` | int | 0 to 250 | PID profile |
| `p_roll` | int | 0 to 250 | PID profile |
| `p_yaw` | int | 0 to 250 | PID profile |
| `pid_at_min_throttle` | enum | `OFF`, `ON` | PID profile |
| `pid_in_tlm` | enum | `OFF`, `ON` |  |
| `pid_process_denom` | int | 1 to 16 |  |
| `pidsum_limit` | int | 100 to 1000 | PID profile |
| `pidsum_limit_yaw` | int | 100 to 1000 | PID profile |
| `pilot_name` | string | 1 to 16 characters |  |
| `pinio_box` | array | array |  |
| `pinio_config` | array | array |  |
| `pitch_expo` | int | 0 to 100 | rate profile |
| `pitch_rate_limit` | int | 200 to 1998 | rate profile |
| `pitch_rc_rate` | int | 1 to 255 | rate profile |
| `pitch_srate` | int | 0 to 255 | rate profile |
| `prearm_allow_rearm` | enum | `OFF`, `ON` |  |
| `profile_name` | string | 1 to 8 characters | PID profile |
| `pwr_on_arm_grace` | int | 0 to 30 |  |
| `quickrates_rc_expo` | enum | `OFF`, `ON` | rate profile |
| `rangefinder_max_range_cm` | int | 50 to 1000 |  |
| `rate_6pos_switch` | enum | `OFF`, `ON` |  |
| `rateprofile_name` | string | 1 to 8 characters | rate profile |
| `rates_type` | enum | `BETAFLIGHT`, `RACEFLIGHT`, `KISS`, `ACTUAL`, `QUICK` | rate profile |
| `rc_smoothing` | enum | `OFF`, `ON` |  |
| `rc_smoothing_auto_factor` | int | 0 to 250 |  |
| `rc_smoothing_auto_factor_throttle` | int | 0 to 250 |  |
| `rc_smoothing_debug_axis` | enum | `ROLL`, `PITCH`, `YAW`, `THROTTLE` |  |
| `rc_smoothing_setpoint_cutoff` | int | 0 to 255 |  |
| `rc_smoothing_throttle_cutoff` | int | 0 to 255 |  |
| `rcdevice_feature` | int | 0 to 65535 |  |
| `rcdevice_init_dev_attempt_interval` | int | 0 to 5000 |  |
| `rcdevice_init_dev_attempts` | int | 0 to 10 |  |
| `rcdevice_protocol_version` | int | 0 to 1 |  |
| `reboot_character` | int | 48 to 126 |  |
| `report_cell_voltage` | enum | `OFF`, `ON` |  |
| `roll_expo` | int | 0 to 100 | rate profile |
| `roll_rate_limit` | int | 200 to 1998 | rate profile |
| `roll_rc_rate` | int | 1 to 255 | rate profile |
| `roll_srate` | int | 0 to 255 | rate profile |
| `rpm_filter_fade_range_hz` | int | 0 to 1000 |  |
| `rpm_filter_harmonics` | int | 0 to 3 |  |
| `rpm_filter_lpf_hz` | int | 100 to 500 |  |
| `rpm_filter_min_hz` | int | 30 to 200 |  |
| `rpm_filter_q` | int | 250 to 3000 |  |
| `rpm_filter_weights` | array | array |  |
| `rssi_channel` | int | 0 to 18 |  |
| `rssi_invert` | enum | `OFF`, `ON` |  |
| `rssi_offset` | int | -100 to 100 |  |
| `rssi_scale` | int | 1 to 255 |  |
| `rssi_smoothing` | int | 0 to 255 |  |
| `rssi_src_frame_errors` | enum | `OFF`, `ON` |  |
| `rssi_src_frame_lpf_period` | int | 0 to 255 |  |
| `runaway_takeoff_deactivate_delay` | int | 100 to 1000 |  |
| `runaway_takeoff_deactivate_throttle_percent` | int | 0 to 100 |  |
| `runaway_takeoff_prevention` | enum | `OFF`, `ON` |  |
| `rx_max_usec` | int | 750 to 2250 |  |
| `rx_min_usec` | int | 750 to 2250 |  |
| `sbus_baud_fast` | enum | `OFF`, `ON` |  |
| `scheduler_debug_task` | int | 0 to 24 |  |
| `scheduler_relax_osd` | int | 0 to 500 |  |
| `scheduler_relax_rx` | int | 0 to 500 |  |
| `serial_update_rate_hz` | int | 100 to 2000 |  |
| `serialmsp_halfduplex` | enum | `OFF`, `ON` |  |
| `serialrx_halfduplex` | enum | `OFF`, `ON` |  |
| `serialrx_inverted` | enum | `OFF`, `ON` |  |
| `serialrx_provider` | enum | `NONE`, `SPEK2048`, `SBUS`, `SUMD`, `SUMH`, `XB-B`, `XB-B-RJ01`, `IBUS`, `JETIEXBUS`, `CRSF`, `SRXL`, `CUSTOM`, `FPORT`, `SRXL2`, `GHST`, `SPEK1024`, `MAVLINK` |  |
| `servo_center_pulse` | int | 750 to 2250 |  |
| `servo_lowpass_hz` | int | 0 to 400 |  |
| `servo_pwm_rate` | int | 50 to 498 |  |
| `simplified_d_gain` | int | 0 to 200 | PID profile |
| `simplified_d_max_gain` | int | 0 to 200 | PID profile |
| `simplified_dterm_filter` | enum | `OFF`, `ON` | PID profile |
| `simplified_dterm_filter_multiplier` | int | 10 to 200 | PID profile |
| `simplified_feedforward_gain` | int | 0 to 200 | PID profile |
| `simplified_gyro_filter` | enum | `OFF`, `ON` |  |
| `simplified_gyro_filter_multiplier` | int | 10 to 200 |  |
| `simplified_i_gain` | int | 0 to 200 | PID profile |
| `simplified_master_multiplier` | int | 0 to 200 | PID profile |
| `simplified_pi_gain` | int | 0 to 200 | PID profile |
| `simplified_pids_mode` | enum | `OFF`, `RP`, `RPY` | PID profile |
| `simplified_pitch_d_gain` | int | 0 to 200 | PID profile |
| `simplified_pitch_pi_gain` | int | 0 to 200 | PID profile |
| `small_angle` | int | 0 to 180 |  |
| `spektrum_sat_bind` | int | 0 to 10 |  |
| `spektrum_sat_bind_autoreset` | enum | `OFF`, `ON` |  |
| `srxl2_baud_fast` | enum | `OFF`, `ON` |  |
| `srxl2_unit_id` | int | 0 to 15 |  |
| `stats_min_armed_time_s` | int | -1 to 127 |  |
| `stats_save_move_limit` | int | 0 to 255 |  |
| `stats_total_dist_m` | int | 0 to 4294967295 |  |
| `stats_total_flights` | int | 0 to 4294967295 |  |
| `stats_total_time_s` | int | 0 to 4294967295 |  |
| `system_hse_mhz` | int | 0 to 30 |  |
| `task_statistics` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_acc_x` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_acc_y` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_acc_z` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_altitude` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_cap_used` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_current` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_distance` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_esc_current` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_esc_rpm` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_esc_temperature` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_esc_voltage` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_fuel` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_ground_speed` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_heading` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_lat_long` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_mode` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_pitch` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_roll` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_temperature` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_vario` | enum | `OFF`, `ON` |  |
| `telemetry_disabled_voltage` | enum | `OFF`, `ON` |  |
| `thr_corr_angle` | int | 1 to 900 |  |
| `thr_corr_value` | int | 0 to 150 |  |
| `thr_expo` | int | 0 to 100 | rate profile |
| `thr_hover` | int | 0 to 100 | rate profile |
| `thr_mid` | int | 0 to 100 | rate profile |
| `throttle_boost` | int | 0 to 100 | PID profile |
| `throttle_boost_cutoff` | int | 5 to 50 | PID profile |
| `throttle_limit_percent` | int | 25 to 100 | rate profile |
| `throttle_limit_type` | enum | `OFF`, `SCALE`, `CLIP` | rate profile |
| `thrust_linear` | int | 0 to 150 | PID profile |
| `timezone_offset_minutes` | int | -780 to 780 |  |
| `tlm_halfduplex` | enum | `OFF`, `ON` |  |
| `tlm_inverted` | enum | `OFF`, `ON` |  |
| `tpa_breakpoint` | int | 1000 to 2000 | PID profile |
| `tpa_low_always` | enum | `OFF`, `ON` | PID profile |
| `tpa_low_breakpoint` | int | 1000 to 2000 | PID profile |
| `tpa_low_rate` | int | 0 to 100 | PID profile |
| `tpa_mode` | enum | `PD`, `D` | PID profile |
| `tpa_rate` | int | 0 to 100 | PID profile |
| `tri_unarmed_servo` | enum | `OFF`, `ON` |  |
| `usb_hid_cdc` | enum | `OFF`, `ON` |  |
| `usb_msc_pin_pullup` | enum | `OFF`, `ON` |  |
| `use_cbat_alerts` | enum | `OFF`, `ON` |  |
| `use_integrated_yaw` | enum | `OFF`, `ON` | PID profile |
| `use_unsynced_pwm` | enum | `OFF`, `ON` |  |
| `use_vbat_alerts` | enum | `OFF`, `ON` |  |
| `vbat_cutoff_percent` | int | 0 to 100 |  |
| `vbat_detect_cell_voltage` | int | 0 to 2000 |  |
| `vbat_display_lpf_period` | int | 1 to 255 |  |
| `vbat_divider` | int | 1 to 255 |  |
| `vbat_duration_for_critical` | int | 0 to 150 |  |
| `vbat_duration_for_warning` | int | 0 to 150 |  |
| `vbat_full_cell_voltage` | int | 100 to 500 | battery profile |
| `vbat_hysteresis` | int | 0 to 250 |  |
| `vbat_max_cell_voltage` | int | 100 to 500 | battery profile |
| `vbat_min_cell_voltage` | int | 100 to 500 | battery profile |
| `vbat_multiplier` | int | 1 to 255 |  |
| `vbat_sag_compensation` | int | 0 to 150 | PID profile |
| `vbat_sag_lpf_period` | int | 1 to 255 |  |
| `vbat_scale` | int | 0 to 255 |  |
| `vbat_warning_cell_voltage` | int | 100 to 500 | battery profile |
| `vcd_h_offset` | int | -32 to 31 |  |
| `vcd_v_offset` | int | -15 to 16 |  |
| `vcd_video_system` | enum | `AUTO`, `PAL`, `NTSC`, `HD` |  |
| `vtx_band` | int | 0 to 8 |  |
| `vtx_channel` | int | 0 to 8 |  |
| `vtx_freq` | int | 0 to 5999 |  |
| `vtx_halfduplex` | enum | `OFF`, `ON` |  |
| `vtx_low_power_disarm` | enum | `OFF`, `ON`, `UNTIL_FIRST_ARM` |  |
| `vtx_pit_mode_freq` | int | 0 to 5999 |  |
| `vtx_power` | int | 0 to 7 |  |
| `vtx_softserial_alt` | enum | `OFF`, `ON` |  |
| `yaw_control_reversed` | enum | `OFF`, `ON` |  |
| `yaw_deadband` | int | 0 to 100 |  |
| `yaw_expo` | int | 0 to 100 | rate profile |
| `yaw_lowpass_hz` | int | 0 to 500 | PID profile |
| `yaw_motors_reversed` | enum | `OFF`, `ON` |  |
| `yaw_rate_limit` | int | 200 to 1998 | rate profile |
| `yaw_rc_rate` | int | 1 to 255 | rate profile |
| `yaw_spin_recovery` | enum | `OFF`, `ON`, `AUTO` |  |
| `yaw_spin_threshold` | int | 500 to 1950 |  |
| `yaw_srate` | int | 0 to 255 | rate profile |
