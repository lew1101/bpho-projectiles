import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 8", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 8 - Bouncing Projectile

**Description:** Use a numerical method assuming constant acceleration motion between small, discrete timesteps (e.g. the "Verlet" method) to compute a projectile trajectory which includes the possibility of a _bounce_. Define the _coefficient of restitution_ $C$ to be the vertical speed of separation divided by the vertical speed of approach. Assume a constant horizontal velocity, and stop the simulation after $N$ bounces. 
"""

model_tab, code_tab, = st.tabs(["Model", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"theta": 45.0, "g": 9.81, "u": 6.0, "h": 2.0, "dt": 0.02, "C": 0.7, "N": 6}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_8(*, theta: float, g: float, u: float, h: float, dt: float, C: float, N: int):
        from math import sin, cos, radians

        ANIMATION_STEP = 1

        rad = radians(theta)

        ux = u * cos(rad)
        uy = u * sin(rad)

        x_list = []
        y_list = []
        total_t = 0

        x = 0
        y = h

        dx = ux * dt

        bounces = 0
        while bounces < N:
            x = x + dx  # since x acceleration is 0, dx is constant
            y = y + uy * dt

            uy = uy - g * dt

            if y < 0:
                y = 0
                uy = -uy * C
                bounces += 1

            total_t += dt
            x_list.append(x)
            y_list.append(y)

        frames_n = len(x_list)
        animation_speed = dt * 1000 * ANIMATION_STEP  # sec -> ms

        fig = go.Figure(
            data=[
                go.Scatter(x=x_list, y=y_list, mode="lines", line_shape='spline'),
                go.Scatter(x=x_list, y=y_list, mode="lines", line_shape='spline'),
            ],
            frames=[
                go.Frame(data=[
                    go.Scatter(x=[x_list[i]],
                               y=[y_list[i]],
                               mode="markers",
                               marker=dict(color="red", size=10))
                ]) for i in range(0, frames_n, ANIMATION_STEP)
            ],
            layout=(config.GO_BASE_LAYOUT | dict(
                title_text="Bouncing Projectile",
                xaxis_title="x (m)",
                yaxis_title="y (m)",
                hovermode="closest",
                width=800,
                height=550,
                autosize=False,
                margin=dict(t=150),
                xaxis=dict(range=[0, max(x_list) + 1], autorange=False),
                yaxis=dict(range=[0, max(y_list) + 1], autorange=False),
                updatemenus=[
                    dict(type="buttons",
                         buttons=[
                             dict(label="Play",
                                  method="animate",
                                  args=[
                                      None,
                                      dict(frame=dict(duration=animation_speed, redraw=False),
                                           fromcurrent=True,
                                           transition=dict(duration=animation_speed,
                                                           easing="quadratic-in-out"))
                                  ]),
                             dict(label="Pause",
                                  method="animate",
                                  args=[[None],
                                        dict(frame=dict(duration=0, redraw=False),
                                             mode="immediate",
                                             transition=dict(duration=0))])
                         ],
                         direction="left",
                         pad=dict(r=10, t=10),
                         xanchor="left",
                         yanchor="top",
                         x=0.06,
                         y=1.18,
                         showactive=False)
                ],
                annotations=[
                    dict(text="Animate:",
                         showarrow=False,
                         x=0,
                         y=1.15,
                         font=dict(size=18),
                         yref="paper",
                         align="right")
                ],
                showlegend=False)),
        )

        return fig, total_t


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_1_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            theta = st.number_input("Launch Angle (deg)",
                                    min_value=0.0,
                                    max_value=90.0,
                                    value=PLOT_DEFAULTS["theta"])
            gravity = st.number_input("Gravity (m⋅s⁻²)", min_value=0.0, value=PLOT_DEFAULTS["g"])
            dt = st.number_input("Time Intervals (s)",
                                 min_value=0.0,
                                 value=PLOT_DEFAULTS["dt"],
                                 step=0.01)
            n_bounces = st.number_input("Number of Bounces",
                                        min_value=1,
                                        max_value=10,
                                        value=PLOT_DEFAULTS["N"])

        with col2:
            vel = st.number_input("Initial Speed (m⋅s⁻¹)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])
            coeff = st.number_input("Coefficient of Restitution",
                                    min_value=0.0,
                                    max_value=1.0,
                                    value=PLOT_DEFAULTS["C"])

        submitted = st.form_submit_button("Generate")

    try:
        fig, total_t = generate_task_8(theta=theta,
                                       g=gravity,
                                       u=vel,
                                       h=height,
                                       dt=dt,
                                       C=coeff,
                                       N=n_bounces)

        st.write("")
        f"""
        #### Calculated Values
        
        **Flight Time**: {total_t:.3f} s
        """
        st.plotly_chart(fig, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

st.divider()
