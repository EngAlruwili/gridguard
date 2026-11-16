# LinkedIn post draft

Review the first-person statements after running and studying the project. Replace
the URL placeholder and adjust the learning claims to match your actual experience.

---

How can we make transformer loading, voltage changes, and thermal behavior easier to understand?

As an electrical engineering student at the University of Jeddah, I am exploring that question with GridGuard: Distribution Transformer Early-Warning Monitor.

GridGuard is an open-source Python and Streamlit prototype that uses synthetic data to visualize apparent-power loading, voltage deviation, and a simplified temperature proxy. Its alerts show the conditions that triggered them, and a replay control lets me explore how the indicators change through a fictional day.

One useful engineering distinction is that the same kVA demand can draw more current when voltage falls. The project keeps current loading separate from kVA loading and uses it in the thermal calculation.

Working through the model helped me connect three-phase calculations with thermal lag, and practice writing tests and documenting assumptions. The stack includes NumPy, pandas, Plotly, Streamlit, and pytest.

This is a learning prototype. The data is synthetic, the thresholds are illustrative, and the temperature output is not a validated operational prediction.

Code, assumptions, and setup instructions: https://github.com/YOUR_USERNAME/gridguard

I would welcome feedback from power engineers and fellow students: what would you test or improve next?

#ElectricalEngineering #PowerSystems #Python #Streamlit #StudentProjects
