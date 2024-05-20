import streamlit as st

import plotly.express as px
import numpy as np

from helpers import apply_custom_plotly_settings

st.set_page_config(page_title="Task 1", layout="wide")

# ==================
r"""
## Task 1 - Projectile Motion  

**Description:** Create a simple model of _drag-free_ projectile motion in a spreadsheet or via a programming language. Inputs are: launch angle from horizontal $\theta$, strength of gravity $g$, launch speed $u$, and launch height $h$. Use a fixed increment of time $\mathrm{d}t$. The graph must automatically update when inputs are changed.
"""

tab1, tab2 = st.tabs(["Model", "Derivations"])

# ==================
# MODEL
# ==================

with tab1:
    body = st.empty()

    with st.expander("See Source Code"), st.echo():

        @apply_custom_plotly_settings
        def generate_task_1(theta: float, g: float, u: float, h: float, dt: float):
            from math import sin, cos, sqrt, radians

            angle = radians(theta)

            ux = u * sin(angle)
            uy = u * cos(angle)

            total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g

            t = np.arange(0, total_t, dt)
            x = ux * t
            y = uy * t - (g * t**2) / 2 + h

            return px.scatter(x=x, y=y,title="Projectile Motion", template="ggplot2")\
                .update_layout(xaxis_title="x (m)", yaxis_title="y (m)")

    with body.container():
        with st.form("task_1_form"):
            "#### **Parameters**"

            col1, col2 = st.columns(2, gap="large")

            with col1:
                theta = st.number_input("Angle (deg)",
                                        min_value=0.0,
                                        max_value=90.0,
                                        value=45.0,
                                        key="theta")
                gravity = st.number_input("Angle (m/s²)", min_value=0.0, value=9.81, key="gravity")
                dt = st.number_input("Time Intervals (s)",
                                     min_value=0.0,
                                     value=0.05,
                                     step=0.01,
                                     key="dt")

            with col2:
                vel = st.number_input("Initial Velocity (m/s)",
                                      min_value=0.0,
                                      value=20.0,
                                      key="vel")
                height = st.number_input("Height (m)", value=2.0, key="height")

            submitted = st.form_submit_button("Generate")

        try:
            fig = generate_task_1(theta, gravity, vel, height, dt)
            st.plotly_chart(fig, config={"displaylogo": False})
        except Exception as e:
            st.exception(e)

# ==================
# DERVIATIONS
# ==================

with tab2:
    r"""
    The dynamics of the projectile can be analyzed by 
    of the  velocity vector of the 
    
    Since there is no force acting on the projectile horizonally, there is no horizontal acceleration. Thus, its $x$ position is equal to its horizontal velocity, $u_x$, times time, $t$.
    $$
    \begin{equation}
    x = u_xt
    \end{equation}
    $$
    
    The projectile is accelerated downwards by gravity
    $$
    \begin{equation}
    y = h + u_yt - \frac{1}{2}gt^2 
    \end{equation}
    $$ 
    """
