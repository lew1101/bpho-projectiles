import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

st.set_page_config(page_title="Task 2", **config.page_config)
 

# ==================
r"""
## Task 2 - Analytical Projectile Motion  

**Description:** Create a more sophisticated exact ("analytical") model using equations for the projectile trajectory. In this case define a equally spaced _array_ of $x$ coordinate values between 0 and the maximum horizontal range, $R$. Plot the trajectory and the apogee.
"""

tab1, tab2 = st.tabs(["Model", "Derivation"])

# ==================
# MODEL
# ==================

with tab1:
    body = st.empty()

    with st.expander("See Source Code"), st.echo():

        def generate_task_2(theta: float, g: float, u: float, h: float, steps: int):
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
                .add_traces(go.Scatter(name="", x=[x_max], y=[y_max], text=["Apogee"], textposition="bottom center", textfont=dict(size=16), marker_symbol="x", marker=dict(size=11), mode='markers+text'))\
                .update_layout(title="Analytical Projectile Motion", xaxis_title="x (m)",  yaxis_title="y (m)",  showlegend=False)
            
            return fig, (x_max, y_max), total_x, total_t

    with body.container():
        with st.form("task_1_form"):
            "#### **Parameters**"

            col1, col2 = st.columns(2, gap="large")

            with col1:
                theta = st.number_input("Angle (deg)", min_value=0.0, max_value=90.0, value=45.0)
                gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=9.81)
                steps = st.number_input("Number of Intervals", min_value=10, max_value=1000, value=30)

            with col2:
                vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=20.0)
                height = st.number_input("Height (m)", value=2.0)

            submitted = st.form_submit_button("Generate")

        try:
            fig, (x_max, y_max), total_x, total_t = generate_task_2(theta, gravity, vel, height, steps)
            
            st.write("")            
            f"""
            #### Calculated Values
            
            **Apogee**: ({x_max:.3f} m, {y_max:.3f} m)
            
            **Range**: {total_x:.3f} m
            
            **Flight Time**: {total_t:.3f} s
            """
            st.plotly_chart(fig, config=config.plotly_chart_config)
        except Exception as e:
            st.exception(e)

# ==================
# DERVIATIONS
# ==================

with tab2:
    r"""
    """
