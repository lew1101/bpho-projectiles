import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 7", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 7 - Range of Projectile vs. Time

**Description:** A curious fact is that the range $R$ of a projectile from the launch point, plotted against time $t$ can, for launch angles greater than about $70.5^\circ$, actually pass through a _local maximum and then a minimum_, before increasing with increasing gradient. Use the derivations to recreate the graphs of $R$ vs $t$. Work out the times, $x$, $y$, and $r$ values for these maxima and minima and plot these via a suitable marker.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"g": 9.81, "u": 10.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_7(*, u: float, g: float):
        from math import sqrt, sin, cos, asin, radians

        fig1 = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Range vs. Time", xaxis_title="t (s)",  yaxis_title="r (m)")

        fig2 = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="XY Graph with Stationary Points", xaxis_title="x (m)",  yaxis_title="y (m)")

        ANGLES = (30, 45, 60, 70.5, 78, 85)

        t = np.linspace(0, 2.5, config.GRAPH_SAMPLES)

        for theta in ANGLES:
            rad = radians(theta)
            range = np.sqrt(u**2 * t**2 - g * t**3 * u * sin(rad) + g**2 * t**4 / 4)

            fig1.add_trace(
                go.Scatter(name=rf"{theta} deg", x=t, y=range, mode="lines", line_shape="spline"))

            if theta > 70.5:
                minima_x = 3 * u / 2 / g * (sin(rad) - sqrt(sin(rad)**2 - 8 / 9))
                maxima_x = 3 * u / 2 / g * (sin(rad) + sqrt(sin(rad)**2 - 8 / 9))

                minima_y = sqrt(u**2 * minima_x**2 - g * minima_x**3 * u * sin(rad) +
                                g**2 * minima_x**4 / 4)
                maxima_y = sqrt(u**2 * maxima_x**2 - g * maxima_x**3 * u * sin(rad) +
                                g**2 * maxima_x**4 / 4)

                fig1.add_trace(go.Scatter(name="minima", x=[minima_x], y=[minima_y], textfont=dict(size=14), marker_symbol="x",
                                marker=dict(size=8, color="lightblue"), mode='markers+text', showlegend=False))\
                    .add_trace(go.Scatter(name="maxima", x=[maxima_x], y=[maxima_y], textfont=dict(size=14), marker_symbol="x",
                                marker=dict(size=8, color="lightgreen"), mode='markers+text', showlegend=False))

            # Using what we did in task 2 for fig2
            ux = u * cos(rad)
            uy = u * sin(rad)

            total_t = uy * 2 / g
            total_x = ux * total_t

            x = np.linspace(0, total_x, config.GRAPH_SAMPLES)
            y = (uy / ux) * x - (g / 2 / ux**2) * x**2

            fig2.add_trace(
                go.Scatter(name=rf"{theta} deg", x=x, y=y, mode="lines", line_shape="spline"))

        # Point of equality (ie having one saddle point instead of a maxima and minima)
        rad = asin(2 * sqrt(2) / 3)
        saddle_x = u / g * sqrt(2)
        saddle_y = sqrt(u**2 * saddle_x**2 - g * saddle_x**3 * u * sin(rad) +
                        g**2 * saddle_x**4 / 4)
        fig1.add_trace(
            go.Scatter(name='saddle point',
                       x=[saddle_x],
                       y=[saddle_y],
                       textfont=dict(size=14),
                       marker_symbol="x",
                       marker=dict(size=8, color="salmon"),
                       mode='markers+text',
                       showlegend=False))

        return fig1, fig2


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_7_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=PLOT_DEFAULTS["u"])

        with col2:
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        submitted = st.form_submit_button("Generate")

    try:
        fig1, fig2 = generate_task_7(u=vel, g=gravity)

        colA, colB = st.columns(2)

        with colA:
            st.plotly_chart(fig1, **config.PLOTLY_CONFIG)

        with colB:
            st.plotly_chart(fig2, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """

st.divider()
