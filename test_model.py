import numpy as np
import pandas as pd
import pytest

from gridguard.model import Transformer, alert_for, evaluate, loading_pct, thermal_proxy, voltage_deviation_pct
from gridguard.synthetic import SCENARIOS, generate_day


def test_known_electrical_values():
    assert loading_pct(400, 500) == pytest.approx(80)
    assert voltage_deviation_pct(380, 400) == pytest.approx(-5)
    frame = generate_day().iloc[:2].copy()
    frame["load_kva"], frame["voltage_v"] = 500.0, 400.0
    result = evaluate(frame)
    assert result["current_a"].iloc[0] == pytest.approx(721.687836, rel=1e-6)
    assert result["current_pct"].iloc[0] == pytest.approx(100)


@pytest.mark.parametrize("values, expected", [
    ((79.9, 79.9, 3.99, 99.9), "NORMAL"),
    ((80, 0, 0, 20), "WATCH"), ((0, 80, 0, 20), "WATCH"),
    ((100, 0, 0, 20), "CRITICAL"), ((0, 100, 0, 20), "CRITICAL"),
    ((0, 0, 4, 20), "WATCH"), ((0, 0, -4, 20), "WATCH"),
    ((0, 0, 6, 20), "CRITICAL"), ((0, 0, -6, 20), "CRITICAL"),
    ((0, 0, 0, 100), "WATCH"), ((0, 0, 0, 120), "CRITICAL"),
])
def test_alert_boundaries(values, expected):
    assert alert_for(*values)[0] == expected


def test_highest_severity_preserves_all_causes():
    status, reason = alert_for(85, 86, -7, 125)
    assert status == "CRITICAL"
    assert all(word in reason for word in ["Apparent-power", "Current", "Voltage", "Hot-spot"])


def test_thermal_equilibrium_and_time_constant():
    t = Transformer()
    oil, hot = thermal_proxy([1, 1], [35, 35], 5, t)
    np.testing.assert_allclose(oil, 90)
    np.testing.assert_allclose(hot, 110)
    oil, _ = thermal_proxy([0, 1], [35, 35], 180, t)
    assert oil[1] == pytest.approx(90 + (oil[0] - 90) * np.exp(-1))
    assert oil[0] < oil[1] < 90


def test_lower_voltage_increases_current_and_thermal_proxy():
    frame = generate_day().iloc[:2].copy()
    frame["load_kva"], frame["voltage_v"] = 400.0, 400.0
    nominal = evaluate(frame)
    frame["voltage_v"] = 380.0
    lower = evaluate(frame)
    assert lower["loading_pct"].iloc[0] == nominal["loading_pct"].iloc[0]
    assert lower["current_pct"].iloc[0] > nominal["current_pct"].iloc[0]
    assert lower["hotspot_proxy_c"].iloc[0] > nominal["hotspot_proxy_c"].iloc[0]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_reproducible_scenarios_and_causal_prefix(scenario):
    frame = generate_day(scenario)
    pd.testing.assert_frame_equal(frame, generate_day(scenario))
    assert len(frame) == 288
    assert frame["data_origin"].str.startswith("SYNTHETIC").all()
    result = evaluate(frame)
    assert np.isfinite(result.select_dtypes("number")).all().all()
    pd.testing.assert_frame_equal(result.iloc[:100], evaluate(frame.iloc[:100]))
    if scenario == "Typical day":
        assert set(result["alert"]) == {"NORMAL"}
    else:
        assert "CRITICAL" in set(result["alert"])


@pytest.mark.parametrize("column, value", [("load_kva", -1), ("voltage_v", 0),
                                          ("ambient_c", np.nan), ("load_kva", np.inf)])
def test_reject_invalid_measurements(column, value):
    frame = generate_day()
    frame.loc[0, column] = value
    with pytest.raises(ValueError):
        evaluate(frame)


def test_reject_irregular_time_and_invalid_rating():
    frame = generate_day()
    frame.loc[1, "timestamp"] = frame.loc[0, "timestamp"]
    with pytest.raises(ValueError):
        evaluate(frame)
    with pytest.raises(ValueError):
        Transformer(rated_kva=0)
    with pytest.raises(ValueError):
        alert_for(np.nan, 0, 0, 20)


def test_larger_rating_keeps_demand_and_reduces_loading():
    frame = generate_day()
    small, large = evaluate(frame, Transformer(rated_kva=500)), evaluate(frame, Transformer(rated_kva=800))
    np.testing.assert_allclose(small["load_kva"], large["load_kva"])
    np.testing.assert_allclose(large["loading_pct"], small["loading_pct"] * 500 / 800)
