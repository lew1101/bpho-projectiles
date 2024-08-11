import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 6", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 6 - Arc Length of Projectile Motion

**Description:** Now update your projectile model with a calculation of the _distance travelled_ by the projectile i.e. the length of the inverted parabolic arc. This can be computed exactly!
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"theta": 60.0, "g": 9.81, "u": 10.0, "h": 2.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_6(*, theta: float, g: float, u: float, h: float):
        from math import sin, cos, sqrt, radians, asin, log, tan

        def calc_dist(rad, x, is_max=False):
            calc_z_part = lambda z: 0.5 * log(abs(sqrt(1 + z**2) + z)) + 0.5 * z * sqrt(1 + z**2)

            if h == 0:
                if is_max:
                    return u**2 / g * (log(1 + sqrt(2)) + sqrt(2)) / 2
                else:
                    return u**2 / g * (log((1 + sin(rad)) / cos(rad)) * cos(rad)**2 + sin(rad))
            else:
                z1 = tan(rad)
                z2 = tan(rad) - g * x / u**2 * (1 + tan(rad)**2)
                calc_z1 = calc_z_part(z1)
                calc_z2 = calc_z_part(z2)
                return u**2 / g / (1 + tan(rad)**2) * (calc_z1 - calc_z2)

        # inputted trajectory
        rad = radians(theta)
        ux = u * cos(rad)
        uy = u * sin(rad)

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        range = ux * total_t
        dist = calc_dist(rad, range)

        original_x = np.linspace(0, range, config.GRAPH_SAMPLES)
        inputted_traj = h + (uy / ux) * original_x - (g / 2 / ux**2) * original_x**2

        # maximize range
        rad_max = asin(1 / sqrt(2 + 2 * g * h / u**2))
        ux = u * cos(rad_max)
        uy = u * sin(rad_max)

        max_range_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        range_max = u / g * sqrt(u**2 + 2 * g * h)
        max_dist = calc_dist(rad, range_max, is_max=True)

        max_range_x = np.linspace(0, range_max, config.GRAPH_SAMPLES)
        max_range_traj = h + (uy / ux) * max_range_x - (g / 2 / ux**2) * max_range_x**2

        fig = go.Figure(
            data=[
                go.Scatter(name="Trajectory",
                           x=original_x,
                           y=inputted_traj,
                           mode="lines",
                           line_shape='spline'),
                go.Scatter(name="Max Range",
                           x=max_range_x,
                           y=max_range_traj,
                           mode="lines",
                           line_dash="dashdot",
                           line_shape='spline'),
                go.Scatter(name="Range",
                           x=[range],
                           y=[0],
                           text=[f"({range:.2f}, {0})"],
                           textposition="top center",
                           textfont=dict(size=14),
                           marker_symbol="x",
                           marker=dict(size=11),
                           mode='markers+text',
                           showlegend=False),
                go.Scatter(name="Max. Range",
                           x=[range_max],
                           y=[0],
                           text=[f"({range_max:.2f}, {0})"],
                           textposition="bottom center",
                           textfont=dict(size=14),
                           marker_symbol="x",
                           marker=dict(size=11),
                           mode='markers+text',
                           showlegend=False),
            ],
            layout=config.GO_BASE_LAYOUT,
        )

        fig.update_layout(title_text="Arc Length of Projectile Motion (with Analytical Model)",
                          xaxis_title="x (m)",
                          yaxis_title="y (m)")

        return fig, range, total_t, rad_max, range_max, max_range_t, dist, max_dist


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_6_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            theta = st.number_input("Launch Angle (deg)",
                                    min_value=0.0,
                                    max_value=90.0,
                                    value=PLOT_DEFAULTS["theta"])
            gravity = st.number_input("Gravity (m⋅s⁻²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        with col2:
            vel = st.number_input("Initial Speed (m⋅s⁻¹)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        submitted = st.form_submit_button("Generate")

    try:
        results = generate_task_6(theta=theta, g=gravity, u=vel, h=height)
        fig, range, total_t, rad_max, range_max, max_range_t, dist, max_dist = results

        from math import degrees

        st.write("")
        f"""
        #### Calculated Values
        
        ##### _Original Trajectory_ 
        
        **Range**: {range:.3f} m
        
        **Flight Time**: {total_t:.3f} s
        
        **Arc Length**: {dist:.3f} m

        """
        st.write("")
        f"""
        ##### _Trajectory Maximizing Range_ 
        
        **Launch Angle**: {degrees(rad_max):.3f} deg
        
        **Maximum Range**: {range_max:.3f} m
        
        **Flight Time**: {max_range_t:.3f} s
        
        **Arc Length**: {max_dist:.3f} m
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
