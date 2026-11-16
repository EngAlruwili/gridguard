from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_dashboard_default_and_controls():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
    assert not app.exception
    assert len(app.metric) == 4
    assert "CRITICAL" in app.error[0].value
    app.sidebar.selectbox[0].select("Typical day").run()
    assert not app.exception
    assert "NORMAL" in app.success[0].value
    app.sidebar.select_slider[0].set_value(800).run()
    app.sidebar.slider[1].set_value(0).run()
    assert not app.exception
    assert len(app.dataframe[0].value) == 1
