import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

st.set_page_config(page_title="Task 3", **config.page_config)

# ==================
r"""
## Task 3 - Projectile to hit X, Yn  

**Description:** Create a new projectile model which is based upon calculating trajectories that are launched from (0, $h$) and pass through a fixed position ($x$, $y$). Calculate the minimum launch speed to achieve this, and hence determine "low ball" and "high ball" trajectories.
"""

tab1, tab2, tab3 = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# MODEL
# =====================

with tab3, st.echo():

    def generate_task_3(target_x: float, target_y: float, g: float, u: float, h: float):
        from math import sqrt, atan

        fig = go.Figure(layout=config.custom_go_layout)\
            .add_traces(go.Scatter(name="target", x=[target_x], y=[target_y], text=[f"({target_x}, {target_y})"], textposition="bottom center",
                                    textfont=dict(size=15), marker_symbol="x", marker=dict(size=11), mode='markers+text'))\
            .update_layout(title="Projectile to hit X, Y", xaxis_title="x (m)", yaxis_title="y (m)")

        SAMPLES = 50
        x = np.linspace(0, target_x, SAMPLES)

        # min vel trajectory
        min_u = sqrt(g) * sqrt(target_y - h + sqrt(target_x**2 + (target_y - h)**2))
        # since only tan(theta) is used in the equation for the parabola, we can optimize by not taking atan and use value directly
        min_tan_theta = (target_y - h + sqrt(target_x**2 + (target_y - h)**2)) / target_x

        min_y_traj = h + x * min_tan_theta - x**2 * g * (1 + min_tan_theta**2) / 2 / min_u**2

        fig.add_trace(go.Scatter(name="min u", x=x, y=min_y_traj, mode="lines",
                                 line_shape='spline'))

        if u > min_u:
            # find high and low ball trajectories
            a = g / 2 / u**2 * target_x**2
            b = -target_x
            c = target_y - h + g / 2 / u**2 * target_x**2

            sqrt_discrim = sqrt(b**2 - 4 * a * c)

            low_tan_theta = (-b -
                             sqrt_discrim) / 2 / a  # we don't take atan for the same reason above
            low_y_traj = h + x * low_tan_theta - x**2 * g * (1 + low_tan_theta**2) / 2 / u**2

            fig.add_trace(
                go.Scatter(name="min u", x=x, y=low_y_traj, mode="lines", line_shape='spline'))

            high_tan_theta = (-b + sqrt_discrim) / 2 / a  # ditto
            high_y_traj = h + x * high_tan_theta - x**2 * g * (1 + high_tan_theta**2) / 2 / u**2

            fig.add_trace(
                go.Scatter(name="high ball", x=x, y=high_y_traj, mode="lines", line_shape='spline'))

            return fig, min_u, atan(min_tan_theta), atan(low_tan_theta), atan(high_tan_theta)
        else:
            return fig, min_u, atan(min_tan_theta), None, None


with tab1:
    with st.form("task_1_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            target_x = st.number_input("Target X (m)", min_value=0.0, value=20.0)
            target_y = st.number_input("Target Y (m)", min_value=0.0, value=10.0)
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=9.81)

        with col2:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=20.0)
            height = st.number_input("Height (m)", value=0.0)

        submitted = st.form_submit_button("Generate")

    try:
        fig, min_u, min_theta, low_theta, high_theta = generate_task_3(
            target_x, target_y, gravity, vel, height)

        sufficient_vel = low_theta is not None and high_theta is not None

        from math import degrees

        st.write("")
        if not sufficient_vel:
            st.warning("The input velocity (m/s) is not sufficient to reach target.", icon="⚠️")
        f"""
        #### Calculated Values
        """

        if sufficient_vel:
            f"""
            **High Ball Launch Angle**: {degrees(high_theta):.2f} deg
            
            **Low Ball Launch Angle**: {degrees(low_theta):.2f} deg
            """

        f"""
        **Minimum Initial Velocity**: {min_u:.2f} m/s
        
        **Launch Angle of Minimum Velocity Parabola**: {degrees(min_theta):.2f} deg
        """

        st.plotly_chart(fig, config=config.plotly_chart_config)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with tab2:
    r"""
    """
