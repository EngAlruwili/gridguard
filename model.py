"""Transparent engineering calculations; not a validated asset model."""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Transformer:
    rated_kva: float = 500.0
    nominal_v: float = 400.0  # Secondary line-to-line RMS voltage
    oil_rise_c: float = 55.0
    winding_rise_c: float = 20.0
    loss_ratio: float = 5.0  # Rated load loss / no-load loss
    tau_minutes: float = 180.0

    def __post_init__(self):
        if not all(np.isfinite(v) and v > 0 for v in vars(self).values()):
            raise ValueError("Transformer parameters must be finite and positive.")


def positive(value, name):
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive.")


def loading_pct(load_kva, rated_kva):
    positive(rated_kva, "rated_kva")
    load = np.asarray(load_kva, dtype=float)
    if not np.isfinite(load).all() or (load < 0).any():
        raise ValueError("Apparent power must be finite and nonnegative.")
    return 100.0 * load / rated_kva


def voltage_deviation_pct(voltage_v, nominal_v):
    positive(nominal_v, "nominal_v")
    voltage = np.asarray(voltage_v, dtype=float)
    if not np.isfinite(voltage).all() or (voltage <= 0).any():
        raise ValueError("Voltage must be finite and positive.")
    return 100.0 * (voltage / nominal_v - 1.0)


def thermal_proxy(current_pu, ambient_c, dt_minutes, transformer):
    """Return top-oil and hot-spot proxies using a first-order oil state.

    Sample zero is initialized at equilibrium with its own input. Subsequent
    sample inputs are treated as constant over the interval ending at that sample.
    """
    positive(dt_minutes, "dt_minutes")
    k = np.asarray(current_pu, dtype=float)
    ambient = np.asarray(ambient_c, dtype=float)
    if k.ndim != 1 or k.size == 0 or k.shape != ambient.shape:
        raise ValueError("Current and ambient must be nonempty matching 1D arrays.")
    if not np.isfinite(k).all() or not np.isfinite(ambient).all() or (k < 0).any():
        raise ValueError("Thermal inputs must be finite; current must be nonnegative.")
    t = transformer
    target = ambient + t.oil_rise_c * ((1 + t.loss_ratio * k**2) / (1 + t.loss_ratio))**0.8
    oil = np.empty_like(target)
    oil[0] = target[0]
    alpha = -np.expm1(-dt_minutes / t.tau_minutes)
    for i in range(1, len(oil)):
        oil[i] = oil[i - 1] + alpha * (target[i] - oil[i - 1])
    return oil, oil + t.winding_rise_c * k**1.6


def alert_for(loading, current_pct, deviation, hotspot_c):
    """Inclusive demo thresholds, highest severity wins, all causes retained."""
    values = [loading, current_pct, deviation, hotspot_c]
    if not np.isfinite(values).all() or loading < 0 or current_pct < 0:
        raise ValueError("Alert inputs must be finite with nonnegative loading/current.")
    rules = [
        ("Apparent-power loading", loading, 80.0, 100.0, "%"),
        ("Current loading", current_pct, 80.0, 100.0, "%"),
        ("Voltage deviation magnitude", abs(deviation), 4.0, 6.0, "%"),
        ("Hot-spot proxy", hotspot_c, 100.0, 120.0, " C"),
    ]
    severity, reasons = 0, []
    for label, value, watch, critical, unit in rules:
        # Tolerance prevents floating point round-off at exact boundaries.
        level = 2 if value >= critical - 1e-9 else 1 if value >= watch - 1e-9 else 0
        if level:
            severity = max(severity, level)
            reasons.append(f"{label}: {value:.1f}{unit} ({['NORMAL', 'WATCH', 'CRITICAL'][level]})")
    return ["NORMAL", "WATCH", "CRITICAL"][severity], "; ".join(reasons) or "Below all demo thresholds"


def evaluate(data, transformer=None):
    """Validate a regular time series and append derived metrics and alerts."""
    t = transformer or Transformer()
    required = ["timestamp", "load_kva", "voltage_v", "ambient_c"]
    if not set(required).issubset(data.columns) or len(data) < 2:
        raise ValueError("Need at least two samples and all required input columns.")
    out = data.copy()
    stamps = pd.to_datetime(out["timestamp"], errors="raise")
    if stamps.isna().any():
        raise ValueError("Timestamps cannot be missing.")
    steps = stamps.diff().dropna().dt.total_seconds().to_numpy() / 60.0
    if (steps <= 0).any() or not np.allclose(steps, steps[0]):
        raise ValueError("Timestamps must be increasing, unique, and regularly spaced.")
    out["timestamp"] = stamps
    out["loading_pct"] = loading_pct(out["load_kva"], t.rated_kva)
    out["voltage_deviation_pct"] = voltage_deviation_pct(out["voltage_v"], t.nominal_v)
    out["current_a"] = out["load_kva"] * 1000.0 / (np.sqrt(3.0) * out["voltage_v"])
    rated_current = t.rated_kva * 1000.0 / (np.sqrt(3.0) * t.nominal_v)
    out["current_pct"] = 100.0 * out["current_a"] / rated_current
    out["top_oil_proxy_c"], out["hotspot_proxy_c"] = thermal_proxy(
        out["current_pct"].to_numpy() / 100.0, out["ambient_c"].to_numpy(), steps[0], t
    )
    alerts = [alert_for(*row) for row in out[
        ["loading_pct", "current_pct", "voltage_deviation_pct", "hotspot_proxy_c"]
    ].itertuples(index=False, name=None)]
    out["alert"], out["reason"] = zip(*alerts)
    return out
