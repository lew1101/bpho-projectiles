import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

st.set_page_config(page_title="Task 1", **config.page_config)

# ==================
r"""
## Task 1 - Projectile Motion  

**Description:** Create a simple model of _drag-free_ projectile motion in a spreadsheet or via a programming language. Inputs are: launch angle from horizontal $\theta$, strength of gravity $g$, launch speed $u$, and launch height $h$. Use a fixed increment of time $\mathrm{d}t$. The graph must automatically update when inputs are changed.
"""

tab1, tab2, tab3 = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# MODEL
# =====================

with tab3, st.echo():

    def generate_task_1(theta: float, g: float, u: float, h: float, dt: float):
        from math import sin, cos, sqrt, radians

        rad = radians(theta)

        ux = u * sin(rad)
        uy = u * cos(rad)

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g

        t = np.arange(0, total_t, dt)
        x = ux * t
        y = h + uy * t - (g / 2) * t**2

        fig = (go.Figure(layout=config.custom_go_layout).add_trace(
            go.Scatter(x=x, y=y, mode="markers")).update_layout(title="Projectile Motion",
                                                                xaxis_title="x (m)",
                                                                yaxis_title="y (m)"))

        return fig, total_t


with tab1:
    with st.form("task_1_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            theta = st.number_input("Launch Angle (deg)", min_value=0.0, max_value=90.0, value=45.0)
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=9.81)
            dt = st.number_input("Time Intervals (s)", min_value=0.0, value=0.05, step=0.01)

        with col2:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=20.0)
            height = st.number_input("Height (m)", value=2.0)

        submitted = st.form_submit_button("Generate")

    try:
        fig, total_t = generate_task_1(theta, gravity, vel, height, dt)

        st.write("")
        f"""
        ##### Calculated Values
        
        **Flight Time**: {total_t:.3f} s
        """
        st.plotly_chart(fig, config=config.plotly_chart_config)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with tab2:
    r"""
    The dynamics of the projectile can be analyzed by decomposing its motion into the x and y axes. Given the initial speed of the projectile $u$ and the launch angle $\theta$, the initial speed in the x direction $u_x$ and the initial speed in the y direction $u_y$ are:
    
    $$
    \begin{gather*}
        u_x = u\cos{\theta} \\
        u_y = u\sin{\theta}
    \end{gather*}
    $$
    
    FirstSince there is no force acting on the projectile horizonally, there is no horizontal acceleration. Thus, its $x$ position is equal to its horizontal velocity, $u_x$, times time, $t$.
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
