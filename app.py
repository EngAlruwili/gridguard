"""Run from the repository root: python -m streamlit run app.py."""

import plotly.graph_objects as go
import streamlit as st

from gridguard.model import Transformer, evaluate
from gridguard.synthetic import SCENARIOS, generate_day

st.set_page_config(page_title="GridGuard", page_icon="⚡", layout="wide")
st.title("GridGuard")
st.subheader("Distribution Transformer Early-Warning Monitor")
st.warning("SYNTHETIC DATA ONLY | Educational demo | Not for operational decisions")

with st.sidebar:
    st.header("Explore a fictional day")
    scenario = st.selectbox("Scenario", SCENARIOS, index=4)
    rating = st.select_slider("Transformer rating (kVA)", options=[315, 500, 630, 800], value=500)
    offset = st.slider("Ambient temperature offset (C)", -10, 10, 0)
    seed = st.number_input("Random seed", min_value=0, max_value=999999, value=42, step=1)
    cursor = st.slider("Replay sample (5-minute steps)", 0, 287, 220)
    st.caption("Changing the rating keeps the same demand. Replay uses only samples up to the selected time.")

transformer = Transformer(rated_kva=float(rating))
raw = generate_day(scenario, int(seed), float(offset))
data = evaluate(raw, transformer)
visible = data.iloc[:cursor + 1]
now = visible.iloc[-1]
st.caption(f"Fictional transformer GG-01 | {rating} kVA | 400 V line-to-line | Balanced three-phase | Asia/Riyadh")
st.write(f"Replay time: **{now['timestamp'].strftime('%Y-%m-%d %H:%M %Z')}**")
cols = st.columns(4)
cols[0].metric("Apparent-power loading", f"{now['loading_pct']:.1f}%", help="100 x load kVA / rated kVA")
cols[1].metric("Secondary voltage", f"{now['voltage_v']:.1f} V", f"{now['voltage_deviation_pct']:+.1f}% vs nominal", delta_color="off")
cols[2].metric("Hot-spot proxy", f"{now['hotspot_proxy_c']:.1f} C", help="Calculated proxy, not a sensor reading.")
cols[3].metric("Current loading", f"{now['current_pct']:.1f}%", help="100 x current / rated current; drives the thermal proxy.")
status = {"NORMAL": st.success, "WATCH": st.warning, "CRITICAL": st.error}[now["alert"]]
status(f"{now['alert']} — {now['reason']}")


def chart(title, series, ylabel, thresholds=()):
    fig = go.Figure()
    colors = ["#0891b2", "#f97316", "#a855f7"]
    for (column, label), color in zip(series, colors):
        fig.add_trace(go.Scatter(x=visible["timestamp"], y=visible[column], name=label,
                                 mode="lines", line=dict(color=color, width=2)))
    for value, label, color in thresholds:
        fig.add_hline(y=value, line_dash="dash", line_color=color,
                      annotation_text=label, annotation_position="top left")
    fig.update_layout(title=title, yaxis_title=ylabel, xaxis_title="Fictional local time (UTC+03:00)",
                      height=360, margin=dict(l=20, r=20, t=100, b=65),
                      legend=dict(orientation="h", y=1.02, yanchor="bottom", font=dict(size=11)),
                      hovermode="x unified")
    st.plotly_chart(fig, width="stretch")


chart("Loading and current", [("loading_pct", "kVA loading"), ("current_pct", "Current loading")], "% of rating",
      [(80, "WATCH 80%", "#d97706"), (100, "CRITICAL 100%", "#dc2626")])
left, right = st.columns(2)
with left:
    chart("Voltage deviation", [("voltage_deviation_pct", "Voltage deviation")], "% of 400 V",
          [(4, "+4% WATCH", "#d97706"), (-4, "-4% WATCH", "#d97706"),
           (6, "+6% CRITICAL", "#dc2626"), (-6, "-6% CRITICAL", "#dc2626")])
with right:
    chart("Temperature proxies and ambient", [("ambient_c", "Ambient (synthetic)"),
          ("top_oil_proxy_c", "Top-oil proxy"), ("hotspot_proxy_c", "Hot-spot proxy")], "Temperature (C)",
          [(100, "WATCH 100 C", "#d97706"), (120, "CRITICAL 120 C", "#dc2626")])

with st.expander("How to interpret the alerts", expanded=True):
    st.markdown("""
| Indicator | WATCH begins | CRITICAL begins |
|---|---:|---:|
| kVA loading or current loading | 80% | 100% |
| Absolute voltage deviation | 4% | 6% |
| Hot-spot temperature proxy | 100 C | 120 C |

All boundaries are inclusive. The highest severity wins, and all active causes are shown.
**NORMAL** means below these demonstration thresholds; it does not certify safety.
**WATCH** invites inspection in the simulation. **CRITICAL** means a higher demo threshold was reached.
These are project choices, not utility limits, protection settings, or compliance criteria.
Early warning means a lower threshold, not a forecast or a guaranteed warning interval.
""")

with st.expander("Engineering assumptions"):
    st.markdown("""
Inputs: total apparent power (kVA), line-to-line RMS voltage (V), and ambient temperature (C).
Balanced sinusoidal three-phase operation is assumed. Current = 1000 S / (sqrt(3) V).
The first-order thermal proxy uses current squared for a loss-related term, a 180-minute oil
time constant, and an instantaneous winding-rise approximation. Initialization assumes
equilibrium at the first sample. No sensor, forecast model, or field calibration is involved.
See `docs/engineering.md` for equations, parameter choices, and limitations.
""")

st.subheader("Replay history")
st.caption("Rows are sample states, not separate incidents. Export contains only the visible replay history.")
st.dataframe(visible[["timestamp", "load_kva", "voltage_v", "ambient_c", "loading_pct",
                      "current_pct", "hotspot_proxy_c", "alert", "reason"]], width="stretch")
export = visible.assign(rated_kva=rating, nominal_v=400.0, ambient_offset_c=offset)
st.download_button("Download synthetic replay CSV", export.to_csv(index=False).encode("utf-8"),
                   "gridguard_synthetic_replay.csv", "text/csv")
