import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 2", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 2 - Analytical Model

**Description:** Create a more sophisticated exact ("analytical") model using equations for the projectile trajectory. In this case define a equally spaced _array_ of $x$ coordinate values between 0 and the maximum horizontal range, $R$. Plot the trajectory and the apogee.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"theta": 45.0, "g": 9.81, "u": 20.0, "h": 2.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_2(*, theta: float, g: float, u: float, h: float):
        from math import sin, cos, sqrt, radians

        fig = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Analytical Model", xaxis_title="x (m)",  yaxis_title="y (m)")

        rad = radians(theta)

        ux = u * cos(rad)
        uy = u * sin(rad)

        xa = ux * uy / g
        ya = h + (uy**2) / 2 / g

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        total_x = ux * total_t

        x = np.linspace(0, total_x, config.GRAPH_SAMPLES)
        y = h + (uy / ux) * x - (g / 2 / ux**2) * x**2


        fig.add_trace(go.Scatter(name="Trajectory", x=x, y=y, mode="lines",  line_shape='spline'))\
           .add_trace(go.Scatter(name="Apogee", x=[xa], y=[ya], text=[f"({xa:.3f}, {ya:.3f})"],
                textposition="bottom center", textfont=dict(size=14), marker_symbol="x", marker=dict(size=11), mode='markers+text'))\

        return fig, (xa, ya), total_x, total_t


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_2_form"):
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
        fig, (x_max, y_max), total_x, total_t = generate_task_2(theta=theta,
                                                                g=gravity,
                                                                u=vel,
                                                                h=height)

        st.write("")
        f"""
        #### Calculated Values
        
        **Apogee**: ({x_max:.3f} m, {y_max:.3f} m)
        
        **Range**: {total_x:.3f} m
        
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
    ##### Finding $y$ as a Function of $x$
    
    The x position of the projectile at any given time $t$ is given by $x = ut\cos{\theta}$. If we isolate $t$ in the equation, we get time $t$ as a function of $x$:
    
    $$
    \begin{equation}
    t = \frac{x}{u\cos{\theta}}
    \end{equation}
    $$
    
    We can then plug this into the equation $y = h + ut\sin{\theta} + \frac{1}{2}gt^2$, allowing us to find $y$ as a function of $x$. 
    
    $$
    \begin{align}
    y &= h + u\sin{\theta}\left(\frac{x}{u\cos{\theta}}\right) + \frac{g}{2}\left(\frac{x}{u\cos{\theta}}\right)^2 \notag \\ 
      &= h + x\tan{\theta} + \frac{g}{2u^2}\sec^2{\theta}
    \end{align}
    $$
    
    ##### Finding the Apogee 
    
    The apogee is maximum of the projectile's trajectory, where the velocity of the projectile in the y direction, $v_y$, is equal to 0. Recall that $v_y = u\sin{\theta} + gt$. Thus:
    
    $$
    \begin{gather*}
    0 = u\sin{\theta} + gt \\
    \Rightarrow t_a = \frac{-u\sin{\theta}}{g}
    \end{gather*}
    $$
    
    where $t_a$ is the time at which the projectile reaches the apogee. From this, we can find the position of the apogee. Recall that $x = ut\cos{\theta}$. Thus, the x coordinate of the apogee $x_a$ is equal to:
    
    $$
    \begin{align}
    x_a &= u\cos{\theta} \cdot t_a \notag \\
        &= u\cos{\theta}\left(\frac{-u\sin{\theta}}{g}\right) \notag \\
        &= \frac{-u^2}{g}\sin{\theta}\cos{\theta}
    \end{align}
    $$
    
    Similarly, recall that $y = h + ut\sin{\theta} + \frac{1}{2}gt^2$. Thus, the y coordinate of the apogee $y_a$ is equal to:
    
    $$
    \begin{align}
    y_a &= h + u\sin{\theta} \cdot t_a + \frac{1}{2}gt_a^2  \notag \\
        &= h + u\sin{\theta}\left(\frac{-u\sin{\theta}}{g}\right) + \frac{g}{2}\left(\frac{-u\sin{\theta}}{g}\right)^2 \notag \\
        &= h - \frac{u^2}{g}\sin^2{\theta} + \frac{u^2}{2g}\sin^2{\theta} \notag \\
        &= h - \frac{u^2}{2g}\sin^2{\theta}
    \end{align}
    $$
    
    ##### Finding the Maximum Horizontal Range $R$ 
    
    From Task 1, we found that the total flight time $T$ of the projectile is equal to:
    
    
    $$
    \begin{align}
    T &= \frac{-u_y - \sqrt{u_y^2-2gh}}{g}  \notag \\
            &= \frac{-u\sin{\theta} - \sqrt{u^2\sin^2{\theta}-2gh}}{g} \notag \\
            &= \frac{-u}{g}\left(\sin{\theta} + \sqrt{\sin^2{\theta} - \frac{2gh}{u^2}}\right)
    \end{align}
    $$
    
    Since the x position of the projectile is equal to $x = ut\cos{\theta}$:
    
    $$
    \begin{align}
    R &= uT\cos{\theta} \notag \\
            &= u\cos{\theta}\cdot \frac{-u}{g}\left(\sin{\theta} + \sqrt{\sin^2{\theta} - \frac{2gh}{u^2}}\right) \notag \\
            &= \frac{-u^2}{g}\left(\sin{\theta}\cos{\theta} + \cos{\theta}\sqrt{\sin^2{\theta} - \frac{2gh}{u^2}}\right)
    \end{align}
    $$
    """

st.divider()
