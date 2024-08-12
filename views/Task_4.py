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

        fig.update_layout(
            title_text="Analytical Model",
            xaxis_title="x (m)",
            yaxis_title="y (m)",
        )

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
            gravity = st.number_input("Gravity (m⋅s⁻²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        with col2:
            vel = st.number_input("Initial Speed (m⋅s⁻¹)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        submitted = st.form_submit_button("Generate")

    try:
        results = generate_task_4(theta=theta, g=gravity, u=vel, h=height)
        fig, range, total_t, rad_max, range_max, max_range_t = results

        from math import degrees

        st.write("")
        f"""
        #### Calculated Values
        
        ##### _Original Trajectory_ 

        **Range**: {range:.3f} m
        
        **Flight Time**: {total_t:.3f} s

        """
        st.write("")
        f"""
        ##### _Trajectory Maximizing Range_    
    
        **Maximum Range**: {range_max:.3f} m
        
        **Launch Angle**: {degrees(rad_max):.3f} deg
        
        **Flight Time**: {max_range_t:.3f} s
        """

        st.plotly_chart(fig, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    The method shown below follows a more elegant geometric approach, but there exists other methods to find the same solution.
    
    ##### Finding the Trajectory of Maximum Range with Same Launch Speed and Height
    
    The velocity at maximum range R is given by the vector equation:
    
    $$
    \begin{equation}
        v = u+gt
    \end{equation}
    $$
    
    where $u$ is the initial velocity, $v$ is the final velocity, $g$ is gravity, and $t$ is the time at which the projectile is at $y=0$. The vectors $u$ and $v$ form a vector triangle, as shown in the diagram below. 
    """
    st.write("")
    with st.columns(3)[1]:
        st.image("./static/images/force_vector.png", width=250)

    st.write("")
    r"""
    We'll first label the angle between $u$ and the horizontal line as $\theta$, and label the angle between $v$ and $u$ as $\phi$. The area of the triangle formed by two vectors is given as half of their cross product:
    
    $$
    \begin{align}
        A &= \frac{1}{2}\vert u \times v \vert \notag \\
        &= \frac{1}{2}uv\sin{\phi}  \\
        &= \frac{1}{2}gt \times u\cos{\theta}
    \end{align}
    $$
    
    Hence:
    $$
    \begin{equation}
        uv\sin{\phi} = gut\cos{\theta}
    \end{equation}
    $$
    
    Since there is no air resistance:
    $$
    \begin{equation}
        R = ut\cos{\theta}
    \end{equation}
    $$
    
    By conservation of energy:
    
    $$
    \begin{gather}
        mgh + \frac{1}{2}mu^2 = \frac{1}{2}mv^2 \notag \\
        \Rightarrow v = \sqrt{2gh+u^2}
    \end{gather}
    $$
    
    Substituting $ut\cos{\theta}$ for $R$ and $v$ for $\sqrt{2gh+u^2}$ in equation 3, we get:
    $$
    \begin{gather}
        \frac{u}{g}\sin{\phi}\sqrt{2gh+u^2} = R \notag\\
        \Rightarrow R = \frac{u^2}{g}\sqrt{1+\frac{2gh}{u^2}}\sin{\phi}
    \end{gather}
    $$
    
    The maximum value for R is when $\sin{\phi}$ is at its maximum, which is when $\sin\phi = 1$. Therefore $\phi=90^\circ$  at max range. Hence, using Pythagoras:
    
    $$
    \begin{align}
        g^2t^2 &= u^2+v^2\notag\\
        \Rightarrow g^2t^2 &= u^2+2gh+u^2\notag\\
        \Rightarrow t &= \frac{u}{g}\sqrt{2+\frac{2gh}{u^2}} 
    \end{align}
    $$
    
    Substituting the new expressions for $R$ and $t$ back into equation 4 gives:
    
    $$
    \begin{align}
        R &= ut\cos{\theta}\notag\\
        \Rightarrow \frac{u^2}{g}\sqrt{1+\frac{2gh}{u^2}} &= u\frac{u}{g}\sqrt{2+\frac{2gh}{u^2}}\cos{\theta}\notag\\
        \Rightarrow \cos{\theta} &= \frac{\sqrt{1+\frac{2gh}{u^2}}}{\sqrt{2+\frac{2gh}{u^2}}}
    \end{align}
    $$
    
    Recall $\sin^2\theta = 1 - \cos^2\theta$:
    
    $$
    \begin{align*}
        \Rightarrow \sin^2\theta &= 1 - \frac{1+\frac{2gh}{u^2}}{2+\frac{2gh}{u^2}} \\
        \Rightarrow \sin^2\theta &= \frac{2+\frac{2gh}{u^2}-1-\frac{2gh}{u^2}}{2+\frac{2gh}{u^2}} \\
        \Rightarrow \sin^2\theta &= \frac{1}{2+\frac{2gh}{u^2}} \\
    \end{align*}
    $$
    
    $$
    \begin{equation}
        \Rightarrow \theta = \arcsin{\left(\frac{1}{2+\frac{2gh}{u^2}}\right)}
    \end{equation}
    $$
    """

st.divider()
