"""Seeded fictional profiles. No field measurements or weather observations."""

import numpy as np
import pandas as pd

SCENARIOS = ("Typical day", "Evening overload", "Undervoltage", "Overvoltage", "Combined stress")


def generate_day(scenario="Combined stress", seed=42, ambient_offset_c=0.0):
    if scenario not in SCENARIOS:
        raise ValueError(f"Choose a scenario from {SCENARIOS}.")
    if not np.isfinite(ambient_offset_c) or not -15 <= ambient_offset_c <= 15:
        raise ValueError("Ambient offset must be within -15 to +15 C.")
    rng = np.random.default_rng(seed)
    stamps = pd.date_range("2026-07-01", periods=288, freq="5min", tz="Asia/Riyadh")
    hour = np.arange(288) / 12.0
    profile = 0.43 + 0.20 * np.exp(-((hour - 15) / 4)**2)
    profile += 0.16 * np.exp(-((hour - 20) / 2.5)**2)
    event = (hour >= 14) & (hour < 21)
    if scenario in ("Evening overload", "Combined stress"):
        profile += 0.65 * event
    # A fixed 500-kVA reference defines demand; changing the dashboard rating
    # does not rescale demand. This makes transformer-sizing comparisons honest.
    load = 500.0 * np.clip(profile + rng.normal(0, 0.008, len(hour)), 0.1, 1.6)
    voltage_pu = 1.01 - 0.025 * load / 500.0 + rng.normal(0, 0.0015, len(hour))
    if scenario in ("Undervoltage", "Combined stress"):
        voltage_pu -= 0.06 * ((hour >= 17) & (hour < 19))
    if scenario == "Overvoltage":
        voltage_pu += 0.08 * ((hour >= 10) & (hour < 12))
    ambient = 35.0 + 6.0 * np.cos(2 * np.pi * (hour - 15) / 24)
    ambient += ambient_offset_c + rng.normal(0, 0.25, len(hour))
    return pd.DataFrame({
        "timestamp": stamps, "load_kva": load, "voltage_v": 400.0 * voltage_pu,
        "ambient_c": ambient, "data_origin": "SYNTHETIC - NOT FIELD MEASUREMENTS",
        "scenario": scenario, "seed": seed,
    })
