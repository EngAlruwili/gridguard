# GridGuard: Distribution Transformer Early-Warning Monitor

A local Python and Streamlit prototype that turns fictional transformer loading,
voltage, and ambient temperature into explainable alert states.

**Synthetic data only. Educational model. Not validated for operational use.**

## Why build this?

A single load curve does not explain every warning: reduced voltage can increase
current at the same apparent power, and temperature responds with a delay.
GridGuard makes these relationships visible without purchasing sensors or accessing
utility data. It is scoped for an electrical engineering student portfolio, including
a University of Jeddah student project; it is not affiliated with or endorsed by the university.

Intended users are students, teaching assistants, and engineers reviewing a learning
prototype. The project demonstrates three-phase calculations, per-unit reasoning,
thermal dynamics, reproducible experiments, and software verification.

## Features

- Five seeded scenarios: typical day, overload, undervoltage, overvoltage, combined stress.
- A fictional 24-hour day at five-minute intervals in Asia/Riyadh time.
- kVA loading, current loading, voltage deviation, and temperature proxy charts.
- NORMAL / WATCH / CRITICAL states with every contributing reason.
- Replay slider, fixed-demand transformer-size comparisons, ambient sensitivity, CSV export.
- Unit tests, a Streamlit smoke test, and a GitHub Actions workflow.
- English portfolio copy, a 72-second vertical-video storyboard, and Arabic SRT subtitles.

## Run locally

Use **Python 3.12**. Run all commands from this repository's root.
No paid data, account, API key, or cloud service is required. Installation needs
internet access; the application works locally after dependencies are installed.

Windows PowerShell, without changing script execution policy:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

macOS / Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m streamlit run app.py
```

Open http://localhost:8501 if the browser does not open automatically. Stop with Ctrl+C.
If Windows redirects `python` to the Store, install Python 3.12 and reopen the terminal,
or use `py -3.12` for the first command if the Python launcher is installed.

## A two-minute demonstration

1. Keep Combined stress, seed 42, 500 kVA, ambient offset 0, and replay sample 220.
2. Inspect the current state and the causes listed in its alert message.
3. Move replay to sample 120, then advance through the afternoon to see thermal lag.
4. Compare Typical day, Undervoltage, and Overvoltage.
5. Increase the rating to 800 kVA: demand stays fixed, while normalized loading changes.
6. Export the visible history; its data-origin column identifies it as synthetic.

## Demonstration thresholds

| Indicator | WATCH | CRITICAL |
|---|---:|---:|
| Apparent-power loading or current loading | >= 80% | >= 100% |
| Absolute voltage deviation | >= 4% | >= 6% |
| Hot-spot temperature proxy | >= 100 C | >= 120 C |

All thresholds are project choices, not Saudi utility requirements, manufacturer
ratings, or IEC/IEEE compliance criteria. The highest severity wins. NORMAL only
means below these thresholds. A step change can skip WATCH entirely: no guaranteed
lead time is claimed. There is no forecast or fault probability model.

## Engineering scope

Defaults: 500 kVA, 400 V secondary line-to-line, balanced sinusoidal three-phase
operation. These are illustrative values, not an asset description from Jeddah.
The thermal output is a **calculated proxy**, not measured winding temperature.
See [engineering notes](docs/engineering.md) for every equation, parameter, input
convention, and limitation, including initialization and loss-model assumptions.

The model does not implement protection, power flow, phase unbalance, harmonics,
insulation aging, cooling controls, or transformer-specific thermal calibration.
Tests verify software behavior; they do not establish field accuracy.

## Repository map

```text
gridguard/
  app.py
  requirements.txt
  README.md
  LICENSE
  .gitignore
  .streamlit/config.toml
  .github/workflows/tests.yml
  gridguard/
    __init__.py
    model.py
    synthetic.py
  tests/
    test_model.py
    test_app.py
  docs/
    engineering.md
    github.md
    linkedin.md
    publishing.md
    verification.md
    video.md
  media/
    narration.txt
    storyboard.json
    subtitles_ar.srt
```

## Portfolio materials

[GitHub description and topics](docs/github.md) · [LinkedIn draft](docs/linkedin.md) ·
[Video storyboard](docs/video.md) · [Publishing steps](docs/publishing.md) ·
[Verification record](docs/verification.md).

Replace the repository URL placeholder before publishing. Review all first-person
learning claims and edit them to match your own work. No upload or publication is
performed by this project. A separate delivery video is a scripted animation of
model outputs with a synthetic English voice; it is not a recorded live dashboard.

## Next experiments

Consider configurable thresholds, event hysteresis, validation with an authorized
anonymized dataset, and a properly parameterized thermal model. Each requires new
tests and clear validation criteria before making stronger claims.

## License

MIT; see [LICENSE](LICENSE). Third-party dependencies retain their own licenses.
The license does not certify engineering suitability.
