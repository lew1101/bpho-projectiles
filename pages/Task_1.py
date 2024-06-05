import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 1", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 1 - Projectile Motion

**Description:** Create a simple model of _drag-free_ projectile motion in a spreadsheet or via a programming language. Inputs are: launch angle from horizontal $\theta$, strength of gravity $g$, launch speed $u$, and launch height $h$. Use a fixed increment of time $\Delta t$. The graph must automatically update when inputs are changed.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"theta": 45.0, "g": 9.81, "u": 20.0, "h": 2.0, "dt": 0.10}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_1(*, theta: float, g: float, u: float, h: float, dt: float):
        from math import sin, cos, sqrt, radians

        rad = radians(theta)

        ux = u * sin(rad)
        uy = u * cos(rad)

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g

        t = np.arange(0, total_t, dt)
        x = ux * t
        y = h + uy * t - (g / 2) * t**2

        fig = go.Figure(layout=config.GO_BASE)\
            .add_trace(go.Scatter(x=x, y=y, mode="markers"))\
            .update_layout(title_text="Projectile Motion", xaxis_title="x (m)", yaxis_title="y (m)")

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
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=PLOT_DEFAULTS["g"])
            dt = st.number_input("Time Intervals (s)",
                                 min_value=0.0,
                                 value=PLOT_DEFAULTS["dt"],
                                 step=0.01)

        with col2:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        submitted = st.form_submit_button("Generate")

    try:
        fig, total_t = generate_task_1(theta=theta, g=gravity, u=vel, h=height, dt=dt)

        st.write("")
        f"""
        #### Calculated Values
        
        **Flight Time**: {total_t:.3f} s
        """
        st.plotly_chart(fig, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    The dynamics of a projectile can be analyzed by decomposing its motion into the x and y axes. Given the initial speed of the projectile $u$ and the launch angle $\theta$, the initial speed in the x direction $u_x$ and the initial speed in the y direction $u_y$ are:
    
    $$
    \begin{gather*}
        u_x = u\cos{\theta} \\
        u_y = u\sin{\theta}
    \end{gather*}
    $$
    
    There is no force acting on the projectile horizonally. Thus, the acceleration of the projectile in the x direction is 0, meaning that the velocity of the projectile in the x direction is constant for the entire duration of the flight. The $x$ position of the projectile at time $t$ is equal to the integral of the velocity in the x direction:
    
    $$
    \begin{align}
    x &= \int_0^t{u_x \,\mathrm{d}t} \notag \\ 
      &= u_x t
    \end{align}
    $$
    
    In the y direction, the projectile is constantly accelerated downwards by gravity $g = -9.81\,\mathrm{m\cdot s^{-2}}$. Thus the y velocity $v_y$ of the projectile is constantly changing, and $v_y$ at time $t$ is equal to the integral the accleration in the y direction:
        
    $$
    \begin{align}
    v_y &= \int_0^t{g \,\mathrm{d}t} \notag \\
        &= u_y + g t
    \end{align}
    $$
    
    where $u_y$ is the initial velocity of the projectile in the y direction. The y position of the projectile at time $t$ is equal to the integral of the velocity in the y direction $v_y$:
    
    $$
    \begin{align}
    y &= \int_0^t{v_y \,\mathrm{d}t}  \notag \\
      &= \int_0^t{\left(u_y + g t\right) \,\mathrm{d}t} \notag \\
      &= h + u_yt + \frac{1}{2}gt^2 
    \end{align} 
    $$ 
    
    where $h$ is the initial height of the projectile. The total flight time of the projectile is a solution of $t$ where $y = 0$ in equation 3:
    
    $$
    \begin{equation*}
    0 = h + u_yt + \frac{1}{2}gt^2 
    \end{equation*}
    $$
    
    The equation is quadratic, which has two solutions. As such, assuming that projectile is moving in the positive direction, the total flight time $T$ is the larger answer.
    
    $$
    \begin{equation}
    T = \frac{-u_y - \sqrt{u_y^2-2gh}}{g}  \qquad (u_x \geq 0)
    \end{equation}
    $$
    """

st.divider()
