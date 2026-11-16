# Verification record

Verification date: 2026-11-16. Environment: Windows, Python 3.12.14.

## Executed checks

- Installed the exact direct dependency versions in `requirements.txt` into an
  isolated local virtual environment. Media tooling was installed separately and
  is not required to run the application.
- Ran `python -m pytest -q` from the repository root: **27 passed in 4.35 seconds**
  on the final run after correcting chart legend spacing and updating width options.
- Covered known electrical values, both polarities of voltage boundaries, exact
  loading/current/thermal thresholds, severity precedence and reason retention,
  thermal equilibrium, the exponential time-constant response, and increased
  current at reduced voltage.
- Checked all five scenarios for deterministic output and causal prefix behavior,
  invalid inputs, duplicate timestamps, and fixed-demand rating comparison.
- The Streamlit AppTest executed the default app and exercised scenario, rating,
  and replay controls, including the one-row replay start.
- Started the actual local Streamlit server and opened it in headless Chrome.
  Three Plotly charts rendered; the browser reported no page errors.
- Clicked the CSV download in the browser and inspected the result: 221 rows for
  samples 0-220, synthetic labels present, and the last timestamp at 18:20 UTC+03:00.
- Inspected the rendered dashboard screenshot and all nine video scene designs.
- Decoded the complete delivery MP4 with FFmpeg without decoding errors. It is
  72 seconds, 1080 x 1920, 30 fps, H.264 video with AAC audio. The final audio is
  48 kHz mono. Arabic captions use Noto Sans Arabic and RTL shaping.

## Reproducible example

Default Combined stress, seed 42, ambient offset 0, 500 kVA, replay sample 220:

| Output | Observed value |
|---|---:|
| kVA loading | 128.066835% |
| Current loading | 139.636572% |
| Voltage deviation | -8.285607% |
| Hot-spot proxy | 144.086558 C |
| Alert | CRITICAL |

These are outputs of the fictional scenario, not performance or accuracy claims.

## Not established by these checks

No field data, sensor integration, physical-model calibration, prediction accuracy,
operational suitability, remote GitHub Actions run, GitHub upload, or LinkedIn
publication was verified or performed. The Linux workflow is supplied but has not
been executed in this delivery environment. Dependency pins cover direct packages;
transitive dependency resolution can still vary between installations.

The video contains a synthetic English voice and scripted charts, not a live
screen recording. A human recording requires subtitle retiming. A final watch on
the intended phone and LinkedIn preview remains part of the publishing checklist.
