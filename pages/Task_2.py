import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 2", **config.page_config)
config.apply_custom_styles()

# ==================
r"""
## Task 2 - Analytical Model

**Description:** Create a more sophisticated exact ("analytical") model using equations for the projectile trajectory. In this case define a equally spaced _array_ of $x$ coordinate values between 0 and the maximum horizontal range, $R$. Plot the trajectory and the apogee.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"theta": 45.0, "g": 9.81, "u": 20.0, "h": 2.0, "steps": 30}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_2(*, theta: float, g: float, u: float, h: float, steps: int):
        from math import sin, cos, sqrt, radians

        rad = radians(theta)

        ux = u * cos(rad)
        uy = u * sin(rad)

        x_max = ux * uy / g
        y_max = h + (uy**2) / 2 / g

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        total_x = ux * total_t

        x = np.linspace(0, total_x, steps)
        y = h + (uy / ux) * x - (g / 2 / ux**2) * x**2

        fig = go.Figure(layout=config.custom_go_layout)\
            .add_trace(go.Scatter(name="", x=x, y=y, mode="lines+markers",  line_shape='spline'))\
            .add_trace(go.Scatter(name="", x=[x_max], y=[y_max], text=["Apogee"], textposition="bottom center",
                                    textfont=dict(size=16), marker_symbol="x", marker=dict(size=11), mode='markers+text'))\
            .update_layout(title_text="Analytical Model", xaxis_title="x (m)",  yaxis_title="y (m)", showlegend=False)

        return fig, (x_max, y_max), total_x, total_t


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_2_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            theta = st.number_input("Launch Angle (deg)",
                                    min_value=0.0,
                                    max_value=90.0,
                                    value=PLOT_DEFAULTS["theta"])
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=PLOT_DEFAULTS["g"])
            steps = st.number_input("Number of Intervals",
                                    min_value=10,
                                    max_value=1000,
                                    value=PLOT_DEFAULTS["steps"])

        with col2:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        submitted = st.form_submit_button("Generate")

    try:
        fig, (x_max, y_max), total_x, total_t = generate_task_2(theta=theta,
                                                                g=gravity,
                                                                u=vel,
                                                                h=height,
                                                                steps=steps)

        st.write("")
        f"""
        #### Calculated Values
        
        **Apogee**: ({x_max:.3f} m, {y_max:.3f} m)
        
        **Range**: {total_x:.3f} m
        
        **Flight Time**: {total_t:.3f} s
        """
        st.plotly_chart(fig, **config.plotly_chart_config)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """
