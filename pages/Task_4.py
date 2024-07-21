import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 4", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 4 - Maximize Projectile Range 

**Description:** Create a new projectile model which compares a trajectory to the trajectory which maximizes horizontal range given the same launch height and launch speed. Inputs are $u$, $h$, $g$ and $\theta$. For the maximum range trajectory you need to calculate the optimum angle. For $h > 0$ note this is not $45^\circ$...
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"theta": 60.0, "g": 9.81, "u": 10.0, "h": 2.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_4(*, theta: float, g: float, u: float, h: float):
        from math import sin, cos, sqrt, radians, asin

        fig = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Analytical Model", xaxis_title="x (m)",  yaxis_title="y (m)")

        # inputted trajectory
        rad = radians(theta)
        ux = u * cos(rad)
        uy = u * sin(rad)

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        range = ux * total_t

        original_x = np.linspace(0, range, config.GRAPH_SAMPLES)
        inputted_traj = h + (uy / ux) * original_x - (g / 2 / ux**2) * original_x**2

        # maximize range
        rad_max = asin(1 / sqrt(2 + 2 * g * h / u**2))
        ux = u * cos(rad_max)
        uy = u * sin(rad_max)

        max_range_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        range_max = u / g * sqrt(u**2 + 2 * g * h)

        max_range_x = np.linspace(0, range_max, config.GRAPH_SAMPLES)
        max_range_traj = h + (uy / ux) * max_range_x - (g / 2 / ux**2) * max_range_x**2

        fig.add_trace(go.Scatter(name="Trajectory", x=original_x, y=inputted_traj, mode="lines", line_shape='spline'))\
           .add_trace(go.Scatter(name="Max Range", x=max_range_x, y=max_range_traj, mode="lines", line_shape='spline'))\
           .add_trace(go.Scatter(name="Range", x=[range], y=[0], text=[f"({range:.2f}, {0})"],
                textposition="top center", textfont=dict(size=14), marker_symbol="x", marker=dict(size=11), mode='markers+text', showlegend=False))\
           .add_trace(go.Scatter(name="Max. Range", x=[range_max], y=[0], text=[f"({range_max:.2f}, {0})"],
                textposition="bottom center", textfont=dict(size=14), marker_symbol="x", marker=dict(size=11), mode='markers+text', showlegend=False))\

        return fig, range, total_t, rad_max, range_max, max_range_t


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_4_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            theta = st.number_input("Launch Angle (deg)",
                                    min_value=0.0,
                                    max_value=90.0,
                                    value=PLOT_DEFAULTS["theta"])
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        with col2:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        submitted = st.form_submit_button("Generate")

    try:
        fig, range, total_t, rad_max, range_max, max_range_t = generate_task_4(theta=theta,
                                                                               g=gravity,
                                                                               u=vel,
                                                                               h=height)

        from math import degrees

        st.write("")
        f"""
        #### Calculated Values

        **Range**: {range:.3f} m
        
        **Flight Time**: {total_t:.3f} s

        """
        st.write("")
        f"""
        ##### _Trajectory Maximizing Range_    
    
        **Maximum Range**: {range_max:.3f} m
        
        **Launch Angle of Trajectory**: {degrees(rad_max):.3f} deg
        
        **Flight Time of Trajectory**: {max_range_t:.3f} s
        """

        st.plotly_chart(fig, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """

st.divider()
