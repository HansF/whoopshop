#!/usr/bin/env python3
"""Betaflight CLI variable registry and response validation.

Betaflight answers an unrecognised `get`/`set` with an error line and carries
on. Nothing in the toolchain checked for that, so a typo in a tuning preset
silently failed to apply. This module catches both classes of mistake:

  * `validate()`  -- reject an unknown variable name before it is sent.
  * `check_response()` -- raise when the board replies with an error.

Names follow Betaflight 4.4 and later. Where a name changed between firmware
versions, the superseded spelling is listed in RENAMED_VARS with its
replacement so the error message can point at the fix.
"""

# Variables this workspace reads or writes. Not the full firmware set -- it is
# the allowlist for commands the tools here generate.
KNOWN_VARS = {
    # Identity and OSD
    "craft_name", "osd_profile", "osd_vbat_pos", "osd_craft_name_pos",
    "osd_rssi_dbm_pos", "osd_warnings_pos",
    # PID controller
    "p_pitch", "i_pitch", "d_pitch", "f_pitch",
    "p_roll", "i_roll", "d_roll", "f_roll",
    "p_yaw", "i_yaw", "d_yaw", "f_yaw",
    "d_max_pitch", "d_max_roll", "d_max_yaw", "d_max_gain",
    "anti_gravity_gain", "anti_gravity_p_gain", "anti_gravity_cutoff_hz",
    "iterm_relax", "iterm_relax_cutoff", "iterm_relax_type", "iterm_windup",
    "pidsum_limit", "pidsum_limit_yaw", "tpa_rate", "tpa_breakpoint", "tpa_mode",
    # Rates
    "rates_type", "roll_rc_rate", "pitch_rc_rate", "yaw_rc_rate",
    "roll_srate", "pitch_srate", "yaw_srate",
    "roll_expo", "pitch_expo", "yaw_expo", "thr_mid", "thr_expo",
    # Motors and ESC
    "motor_pwm_protocol", "motor_pwm_rate", "motor_poles", "motor_idle",
    "motor_output_limit", "dshot_bidir", "dshot_burst", "dshot_bitbang",
    "min_check", "max_check", "min_command", "max_throttle",
    "dyn_idle_min_rpm", "dyn_idle_p_gain", "dyn_idle_i_gain", "dyn_idle_d_gain",
    "dyn_idle_max_increase",
    # Filters
    "gyro_lpf1_static_hz", "gyro_lpf2_static_hz",
    "gyro_lpf1_dyn_min_hz", "gyro_lpf1_dyn_max_hz",
    "dterm_lpf1_static_hz", "dterm_lpf2_static_hz",
    "dterm_lpf1_dyn_min_hz", "dterm_lpf1_dyn_max_hz",
    "dyn_notch_count", "dyn_notch_q", "dyn_notch_min_hz", "dyn_notch_max_hz",
    "rpm_filter_harmonics", "rpm_filter_q", "rpm_filter_min_hz",
    "yaw_lowpass_hz",
    # Receiver and telemetry
    "serialrx_provider", "serialrx_inverted", "serialrx_halfduplex",
    "crsf_use_negotiated_baud", "rssi_channel", "rssi_scale", "rssi_offset",
    "rx_min_usec", "rx_max_usec", "mid_rc", "deadband", "yaw_deadband",
    # Blackbox
    "blackbox_device", "blackbox_mode", "blackbox_sample_rate",
    "blackbox_high_resolution", "blackbox_disable_gyro", "blackbox_disable_rpm",
    "blackbox_disable_motors",
    # Video transmitter
    "vtx_band", "vtx_channel", "vtx_power", "vtx_pit_mode", "vtx_freq",
    # Battery
    "vbat_min_cell_voltage", "vbat_max_cell_voltage", "vbat_warning_cell_voltage",
    "vbat_full_cell_voltage", "battery_meter", "bat_capacity",
    "force_battery_cell_count", "vbat_sag_compensation",
    # Safety and failsafe
    "small_angle", "failsafe_procedure", "failsafe_throttle", "failsafe_delay",
    "gyro_cal_on_first_arm", "runaway_takeoff_prevention",
}

# Superseded or invented names -> what to use instead.
RENAMED_VARS = {
    "dynamic_idle_min_rpm": "dyn_idle_min_rpm",
    "idle_min_rpm": "dyn_idle_min_rpm",
    "crsf_use_painless_telemetry": "crsf_use_negotiated_baud",
    "rx_serial_protocol": "serialrx_provider",
    "telemetry_disabled": "the `feature TELEMETRY` command (not a variable)",
    "map": "the bare `map AETR1234` command (not a variable)",
    "dterm_lowpass_hz": "dterm_lpf1_static_hz",
    "gyro_lowpass_hz": "gyro_lpf1_static_hz",
    "d_setpoint_weight": "f_pitch / f_roll / f_yaw",
}

# CLI commands that are not variables and must never be wrapped in get/set.
BARE_COMMANDS = {
    "status", "version", "diff", "dump", "defaults", "save", "exit",
    "map", "motor", "feature", "beeper", "resource", "mixer", "tasks",
    "flash_info", "flash_erase", "flash_read", "flash_write", "msc",
    "bl", "dfu", "mcu_id", "serial", "aux", "adjrange", "rxrange",
    "led", "color", "mode_color", "play_sound", "profile", "rateprofile",
    "bind_rx", "vtx", "vtxtable", "escprog", "gyroregisters", "batch",
}

# Substrings Betaflight emits when it rejects input.
ERROR_MARKERS = (
    "Invalid name",
    "Invalid value",
    "Unknown command",
    "Parse error",
    "ERROR:",
)


class UnknownVariableError(ValueError):
    """Raised when a command targets a variable Betaflight will not accept."""


class CliResponseError(RuntimeError):
    """Raised when the Flight Controller rejects a command."""


def variable_name(command):
    """Return the variable a `get`/`set` command targets, or None.

    >>> variable_name("set dyn_idle_min_rpm = 30")
    'dyn_idle_min_rpm'
    >>> variable_name("status") is None
    True
    """
    parts = command.strip().split(None, 1)
    if len(parts) != 2 or parts[0].lower() not in ("get", "set"):
        return None
    remainder = parts[1]
    return remainder.split("=", 1)[0].strip()


def validate(commands):
    """Check commands against the registry, returning a list of problems.

    An empty list means every command looks sendable.
    """
    problems = []
    for cmd in commands:
        name = variable_name(cmd)
        if name is None:
            continue
        if name in RENAMED_VARS:
            problems.append(
                f"`{cmd}` uses '{name}', which this firmware does not accept. "
                f"Use {RENAMED_VARS[name]}."
            )
        elif name in BARE_COMMANDS:
            problems.append(
                f"`{cmd}` wraps '{name}' in get/set, but '{name}' is a bare CLI "
                f"command. Send `{name}` on its own instead."
            )
        elif name not in KNOWN_VARS:
            problems.append(
                f"`{cmd}` targets unknown variable '{name}'. Add it to "
                f"KNOWN_VARS in tools/bf_vars.py if your firmware supports it."
            )
    return problems


def assert_valid(commands):
    """Raise UnknownVariableError if any command would be rejected."""
    problems = validate(commands)
    if problems:
        raise UnknownVariableError(
            "Refusing to send commands the flight controller will reject:\n  - "
            + "\n  - ".join(problems)
        )


def check_response(command, output):
    """Raise CliResponseError when the FC's reply signals a rejection."""
    for marker in ERROR_MARKERS:
        if marker in output:
            line = next(
                (l.strip() for l in output.splitlines() if marker in l), output.strip()
            )
            raise CliResponseError(f"Flight controller rejected `{command}`: {line}")


def check_responses(results):
    """Apply check_response across a {command: output} mapping."""
    for command, output in results.items():
        check_response(command, output)
