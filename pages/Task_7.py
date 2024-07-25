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

        ANGLES = (30, 45, 60, 70.5, 78, 85)

        fig1 = go.Figure(layout=config.GO_BASE_LAYOUT.update(
            title_text="Range vs. Time", xaxis_title="t (s)", yaxis_title="r (m)"))

        fig2 = go.Figure(layout=config.GO_BASE_LAYOUT.update(
            title_text="XY Graph", xaxis_title="x (m)", yaxis_title="y (m)"))

        t = np.linspace(0, 2.5, config.GRAPH_SAMPLES)

        for theta in ANGLES:
            rad = radians(theta)
            range = np.sqrt(u**2 * t**2 - g * t**3 * u * sin(rad) + g**2 * t**4 / 4)

            fig1.add_trace(
                go.Scatter(name=rf"{theta} deg", x=t, y=range, mode="lines", line_shape="spline"))

            ux = u * cos(rad)
            uy = u * sin(rad)

            # Using what we did in task 2 for figure
            total_t = uy * 2 / g
            total_x = ux * total_t

            x = np.linspace(0, total_x, config.GRAPH_SAMPLES)
            y = (uy / ux) * x - (g / 2 / ux**2) * x**2

            fig2.add_trace(
                go.Scatter(name=rf"{theta} deg", x=x, y=y, mode="lines", line_shape="spline"))

            if theta > 70.5:
                minima_x = 3 * u / 2 / g * (sin(rad) - sqrt(sin(rad)**2 - 8 / 9))
                minima_y = sqrt(u**2 * minima_x**2 - g * minima_x**3 * u * sin(rad) +
                                g**2 * minima_x**4 / 4)

                maxima_x = 3 * u / 2 / g * (sin(rad) + sqrt(sin(rad)**2 - 8 / 9))
                maxima_y = sqrt(u**2 * maxima_x**2 - g * maxima_x**3 * u * sin(rad) +
                                g**2 * maxima_x**4 / 4)

                fig1.add_traces(data=[
                    go.Scatter(name="Minima",
                               x=[minima_x],
                               y=[minima_y],
                               textfont=dict(size=14),
                               marker_symbol="x",
                               marker=dict(size=8, color="deepskyblue"),
                               mode='markers+text',
                               showlegend=False),
                    go.Scatter(name="Maxima",
                               x=[maxima_x],
                               y=[maxima_y],
                               textfont=dict(size=14),
                               marker_symbol="x",
                               marker=dict(size=8, color="limegreen"),
                               mode='markers+text',
                               showlegend=False)
                ])

                # plot corresponding point on XY graph
                xy_minima_x = ux * minima_x
                xy_minima_y = uy * minima_x - g / 2 * minima_x**2

                xy_maxima_x = ux * maxima_x
                xy_maxima_y = uy * maxima_x - g / 2 * maxima_x**2

                fig2.add_traces(data=[
                    go.Scatter(name="R vs. t Minima",
                               x=[xy_minima_x],
                               y=[xy_minima_y],
                               textfont=dict(size=14),
                               marker_symbol="x",
                               marker=dict(size=8, color="deepskyblue"),
                               mode='markers+text',
                               showlegend=False),
                    go.Scatter(name="R vs. t Maxima",
                               x=[xy_maxima_x],
                               y=[xy_maxima_y],
                               textfont=dict(size=14),
                               marker_symbol="x",
                               marker=dict(size=8, color="limegreen"),
                               mode='markers+text',
                               showlegend=False)
                ])

        # Point of equality (ie having one saddle point instead of a maxima and minima)
        rad = asin(2 * sqrt(2) / 3)

        saddle_x = u / g * sqrt(2)
        saddle_y = sqrt(u**2 * saddle_x**2 - g * saddle_x**3 * u * sin(rad) +
                        g**2 * saddle_x**4 / 4)
        fig1.add_trace(
            go.Scatter(name='Saddle Point',
                       x=[saddle_x],
                       y=[saddle_y],
                       textfont=dict(size=14),
                       marker_symbol="x",
                       marker=dict(size=8, color="salmon"),
                       mode='markers+text',
                       showlegend=False))

        # plot corresponding point on XY graph
        xy_maxima_x = u * cos(rad) * saddle_x
        xy_maxima_y = u * sin(rad) * saddle_x - g / 2 * saddle_x**2

        fig2.add_trace(
            go.Scatter(name='Saddle Point',
                       x=[xy_maxima_x],
                       y=[xy_maxima_y],
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

        st.plotly_chart(fig1, **config.PLOTLY_CONFIG)
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
