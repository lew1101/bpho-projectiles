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
    This model is built upon Task 2$\\$
    Please do refer to Task 2 for queries on generation of inputted trajectory
    
    The method shown follows a geometric approach but there are various methods to achieve the same derivation
    
    ##### Finding the Trajectory of Maximum Range with Same Launch Speed and Height
    
    The velocity at maximum range R is given by the vector equation:
    
    $$
    \begin{equation}
        \bold{v} = \bold{u}+\bold{g}t
    \end{equation}
    $$
    
    Therefore, a vector triangle can be formed!
    """
    
    st.columns(9)[4].image('./static/images/Vector Diagram.png')
    #Don't understand why doesn't work, if u have time, solve it: caption='Credit: BPhO Website pdf https://www.bpho.org.uk/bpho/computational-challenge/BPhO_CompPhys2024_Projectilesa.pdf'
    
    r"""
    We'll first label the angle between $\bold{u}$ and the horizontal line as $\theta\\$ 
    And label the angle between $\bold{v}$ and $\bold{u}$ as $\phi$: $\\$
    The area of such triangle can be computed in 2 ways:
    
    $$
    \begin{equation}
        A = \frac{1}{2}uv\sin{\phi}
    \end{equation}
    $$
    
    As well as:
    
    $$
    \begin{equation}
        A = \frac{1}{2}gt \times u\cos{\theta}
    \end{equation}
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
    \begin{align}
        mgh + \frac{1}{2}mu^2 &= \frac{1}{2}mv^2\notag\\
        \Rightarrow v &= \sqrt{2gh+u^2}
    \end{align}
    $$
    
    Substituting $ut\cos{\theta}$ for $R$ and $v$ for $\sqrt{2gh+u^2}$ in equation 3, we get:
    $$
    \begin{align}
        \frac{u}{g}\sin{\phi}\sqrt{2gh+u^2} &= R\notag\\
        \Rightarrow R &= \frac{u^2}{g}\sqrt{1+\frac{2gh}{u^2}}\sin{\phi}
    \end{align}
    $$
    
    As the largest R value corresponds to $\sin{\phi} = 1$, $\phi = 90\\$
    Therefore the velocity triangle is right angled at max range$\\$
    Hence we can calculate time of flight using pythagoras
    
    $$
    \begin{align}
        g^2t^2 &= u^2+v^2\notag\\
        \Rightarrow g^2t^2 &= u^2+2gh+u^2\notag\\
        \Rightarrow t &= \frac{u}{g}\sqrt{2+\frac{2gh}{u^2}} 
    \end{align}
    $$
    
    Subbing the new expressions for $R$ and $t$ back into equation 4 gives:
    
    $$
    \begin{align}
        R &= ut\cos{\theta}\notag\\
        \Rightarrow \frac{u^2}{g}\sqrt{1+\frac{2gh}{u^2}} &= u\frac{u}{g}\sqrt{2+\frac{2gh}{u^2}}\cos{\theta}\notag\\
        \Rightarrow \cos{\theta} &= \frac{\sqrt{1+\frac{2gh}{u^2}}}{\sqrt{2+\frac{2gh}{u^2}}}
    \end{align}
    $$
    
    Remember that $sin^2\theta = 1 - cos^2\theta$:
    
    $$
    \begin{align}
        \Rightarrow \sin^2\theta &= 1 - \frac{1+\frac{2gh}{u^2}}{2+\frac{2gh}{u^2}}\notag\\
        \Rightarrow \sin^2\theta &= \frac{2+\frac{2gh}{u^2}-1-\frac{2gh}{u^2}}{2+\frac{2gh}{u^2}}\notag\\
        \Rightarrow \sin^2\theta &= \frac{1}{2+\frac{2gh}{u^2}}\notag\\
        \Rightarrow \theta & = \arcsin{\left(\frac{1}{2+\frac{2gh}{u^2}}\right)}
    \end{align}
    $$
    """

st.divider()
