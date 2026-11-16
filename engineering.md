# Engineering design and limitations

## Problem, users, and value

Distribution-transformer loading, voltage, and temperature are connected but not
interchangeable indicators. GridGuard gives students and teaching assistants a
repeatable way to explore them, and gives a portfolio reviewer inspectable code
instead of a static concept slide. It supports discussion of transformer capacity,
current, loss-related heating, thermal lag, and explainable monitoring logic.

## Inputs and conventions

- `load_kva`: total three-phase apparent power magnitude, not real power in kW.
- `voltage_v`: secondary line-to-line RMS voltage; never line-to-neutral voltage.
- `ambient_c`: fictional ambient temperature in degrees Celsius.
- `timestamp`: strictly increasing, unique, regular timestamps. The demo uses 5 minutes.
- Default transformer: 500 kVA and 400 V. Assume balanced sinusoidal operation.
- No power factor is required because apparent power is already supplied. If adapting
  the project to real power, obtain a defensible power factor; do not equate kW to kVA.

## Electrical calculations

Let S be total apparent power in kVA, Sr rated apparent power in kVA, V line-to-line
voltage in V, and Vn nominal line-to-line voltage in V.

```text
kVA loading (%) = 100 S / Sr
Voltage deviation (%) = 100 (V / Vn - 1)
I (A) = 1000 S / (sqrt(3) V)
Ir (A) = 1000 Sr / (sqrt(3) Vn)
K = I / Ir = (S / Sr) (Vn / V)
Current loading (%) = 100 K
```

At 500 kVA and 400 V, I is approximately 721.69 A. If voltage falls to 380 V at
the same apparent power, current increases to approximately 759.67 A. The kVA
loading stays 100%, while current loading becomes approximately 105.26%.
This distinction is why current ratio K drives the thermal proxy.
The balanced three-phase relation follows the
[Schneider Electric Electrical Installation Guide](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)).

## Simplified thermal proxy

This is a deliberately reduced dynamic model with an oil-temperature state and
an instantaneous winding gradient. It is inspired by common loss-based thermal
model structures but does **not** implement or certify compliance with a standard.

```text
Oil target[n] = Ambient[n] + 55 ((1 + 5 K[n]^2) / 6)^0.8
alpha = 1 - exp(-dt_minutes / 180)
Oil[0] = Oil target[0]
Oil[n] = Oil[n-1] + alpha (Oil target[n] - Oil[n-1])
Hot-spot proxy[n] = Oil[n] + 20 K[n]^1.6
```

Temperature rises have units of kelvin (numerically equal to differences in C).
Absolute temperatures are reported in C. The 55 K rated oil rise, 20 K rated
winding-to-oil gradient, load-loss/no-load-loss ratio of 5, 180-minute time constant,
and exponents 0.8 and 1.6 are **illustrative parameters**, not measurements.
All transformer ratings in the UI retain these same thermal parameters; therefore
the rating control is a normalized sensitivity experiment, not equipment selection.

The oil state filters the absolute target temperature, including ambient changes.
Sample zero assumes equilibrium at its own input; no earlier history is known.
Each subsequent sample's input is treated as held over the interval ending at
that sample. This explicit discrete convention affects transients. A full
constant-input time constant moves the oil state 1 - exp(-1), about 63.2%, toward
its target. At K=1 and ambient 35 C, equilibrium oil is 90 C and hot-spot proxy is
110 C. At K=0 there is still a no-load heating term; the transformer is assumed energized.

The winding gradient has no separate time constant. A sudden current change can
therefore cause an unrealistic instantaneous jump in hot-spot proxy. Loss ratio
is fixed; core loss changes with voltage and frequency are omitted.
Research thermal models use transformer-specific parameters and measured responses;
see the experimental paper
[Experimental study of dynamic thermal behaviour of an 11 kV distribution transformer](https://doi.org/10.1049/oap-cired.2017.1102).
This reference provides context; it does not validate GridGuard or supply these defaults.

## Warning policy

| Indicator | WATCH inclusive | CRITICAL inclusive |
|---|---:|---:|
| kVA loading | 80% | 100% |
| Current loading | 80% | 100% |
| Magnitude of voltage deviation | 4% | 6% |
| Hot-spot proxy | 100 C | 120 C |

Take the maximum severity across all four indicators and retain all active reasons.
At exactly 100% loading the project deliberately enters CRITICAL; this label does
not imply that rated loading is inherently unsafe. The labels are demonstration
categories, not protection actions. A numerical tolerance of 1e-9 handles exact
floating-point boundaries.

There is no persistence filter or hysteresis; noisy samples can change state
frequently. Rows count sample states, not incidents. WATCH provides a lower
threshold that may be reached earlier in a gradual rise, but no time-to-failure,
forecast, probabilistic risk, or guaranteed lead time is produced. An abrupt
voltage event can enter CRITICAL directly.

## Synthetic data design

The generator creates 288 samples on a fictional July day, tagged as synthetic
in every row. A fixed seed makes repeated experiments reproducible.
Demand uses a 0.43 baseline with smooth afternoon/evening peaks, scaled by a fixed
500-kVA reference plus small Gaussian variation. An overload adds 0.65 per unit
from 14:00 to 21:00. Voltage has a small demand-correlated reduction and noise;
the undervoltage case adds -0.06 per unit from 17:00 to 19:00, and overvoltage
adds +0.08 per unit from 10:00 to 12:00. These are imposed disturbances, not load-flow results.
Ambient uses 35 + 6 cos(2 pi (hour - 15)/24), optional offset, and small noise.
It represents a plausible hot-day teaching pattern, **not Jeddah weather data**.

Changing the transformer rating leaves the input demand and voltage unchanged.
Changing ambient temperature changes the thermal output but does not feed back
into demand. The model is deliberately one-way. The dashboard shows history only
up to the replay cursor; calculations of a prefix do not depend on future rows.
Invalid, missing, duplicate, or irregular inputs raise an error rather than
silently classifying them as NORMAL. No general-purpose file importer is included.

## Limits and responsible interpretation

No real sensor measurements, field calibration, accuracy estimate, or industrial
endorsement exists. Excluded effects include phase unbalance, harmonics, frequency
variation, reverse flow direction, tap changers, protection coordination, cooling
stages, moisture, oil condition, insulation aging, solar gain, and enclosure airflow.
Software tests establish arithmetic and interface behavior, not physical accuracy.
Use only for education and a portfolio demonstration. Operational work would need
authorized measurements, manufacturer parameters, verified instrumentation,
applicable standards, validation against independent data, and engineering review.

## Why it fits power engineering

The core work is interpreting kVA ratings, RMS voltage, current stress, heat
generation, and delayed temperature response. Python is the means to make those
relationships testable and visible. Useful student extensions include sensitivity
analysis of time constant, explicit unbalance metrics with per-phase data, and
comparisons between measured and estimated temperature when authorized data exists.
