import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 7", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 7 - Range of Projectile vs. Time

**Description:** A curious fact is that the range $R$ of a projectile from the launch point, plotted against time $t$ can, for launch angles greater than about $70.5^\circ$, actually pass through a _local maximum and then a minimum_, before increasing with increasing gradient. Use the derivations to recreate the graphs of $R$ vs $t$. Work out the times, $x$, $y$, and $r$ values for these maxima and minima and plot these via a suitable marker.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"g": 9.81, "u": 10.0, "h": 2.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_7(*, u: float, g: float, h: float):
        from math import sqrt, sin, cos, asin, radians

        ANGLES = (30, 45, 60, 70.5, 78, 85)

        fig1 = go.Figure(
            layout=(config.GO_BASE_LAYOUT |
                    dict(title_text="Range vs. Time", xaxis_title="t (s)", yaxis_title="r (m)")))

        fig2 = go.Figure(layout=dict(**config.GO_BASE_LAYOUT,
                                     title_text="XY Graph",
                                     xaxis_title="x (m)",
                                     yaxis_title="y (m)"))

        minima_x_list = []
        minima_y_list = []

        maxima_x_list = []
        maxima_y_list = []

        xy_minima_x_list = []
        xy_minima_y_list = []

        xy_maxima_x_list = []
        xy_maxima_y_list = []

        for theta in ANGLES:
            rad = radians(theta)

            ux = u * cos(rad)
            uy = u * sin(rad)

            total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g

            t = np.linspace(0, total_t, config.GRAPH_SAMPLES)
            range = np.sqrt(u**2 * t**2 - g * t**3 * u * sin(rad) + g**2 * t**4 / 4)

            fig1.add_trace(
                go.Scatter(name=rf"{theta} deg", x=t, y=range, mode="lines", line_shape="spline"))

            # Using what we did in task 2 for figure

            total_x = ux * total_t

            x = np.linspace(0, total_x, config.GRAPH_SAMPLES)
            y = h + (uy / ux) * x - (g / 2 / ux**2) * x**2

            fig2.add_trace(
                go.Scatter(name=rf"{theta} deg", x=x, y=y, mode="lines", line_shape="spline"))

            if theta > 70.5:
                minima_x_list.append(minima_x := 3 * u / 2 / g *
                                     (sin(rad) - sqrt(sin(rad)**2 - 8 / 9)))
                minima_y_list.append(
                    sqrt(u**2 * minima_x**2 - g * minima_x**3 * u * sin(rad) +
                         g**2 * minima_x**4 / 4))

                maxima_x_list.append(maxima_x := 3 * u / 2 / g *
                                     (sin(rad) + sqrt(sin(rad)**2 - 8 / 9)))
                maxima_y_list.append(
                    sqrt(u**2 * maxima_x**2 - g * maxima_x**3 * u * sin(rad) +
                         g**2 * maxima_x**4 / 4))

                xy_minima_x_list.append(ux * minima_x)
                xy_minima_y_list.append(uy * minima_x - g / 2 * minima_x**2 + h)

                xy_maxima_x_list.append(ux * maxima_x)
                xy_maxima_y_list.append(uy * maxima_x - g / 2 * maxima_x**2 + h)

        fig1.add_traces(data=[
            go.Scatter(
                name="Minima",
                x=minima_x_list,
                y=minima_y_list,
                textfont=dict(size=14),
                marker_symbol="x",
                marker=dict(size=8, color="deepskyblue"),
                mode='markers+text',
            ),
            go.Scatter(
                name="Maxima",
                x=maxima_x_list,
                y=maxima_y_list,
                textfont=dict(size=14),
                marker_symbol="x",
                marker=dict(size=8, color="limegreen"),
                mode='markers+text',
            )
        ])

        # plot corresponding points on XY graph
        fig2.add_traces(data=[
            go.Scatter(
                name="R vs. t Minima",
                x=xy_minima_x_list,
                y=xy_minima_y_list,
                textfont=dict(size=14),
                marker_symbol="x",
                marker=dict(size=8, color="deepskyblue"),
                mode='markers+text',
            ),
            go.Scatter(
                name="R vs. t Maxima",
                x=xy_maxima_x_list,
                y=xy_maxima_y_list,
                textfont=dict(size=14),
                marker_symbol="x",
                marker=dict(size=8, color="limegreen"),
                mode='markers+text',
            )
        ])

        # Point of equality (ie having one saddle point instead of a maxima and minima)
        rad = asin(2 * sqrt(2) / 3)

        saddle_x = u / g * sqrt(2)
        saddle_y = sqrt(u**2 * saddle_x**2 - g * saddle_x**3 * u * sin(rad) +
                        g**2 * saddle_x**4 / 4)
        fig1.add_trace(
            go.Scatter(
                name='Saddle Point',
                x=[saddle_x],
                y=[saddle_y],
                textfont=dict(size=14),
                marker_symbol="x",
                marker=dict(size=8, color="salmon"),
                mode='markers+text',
            ))

        # plot corresponding point on XY graph
        xy_maxima_x = u * cos(rad) * saddle_x
        xy_maxima_y = u * sin(rad) * saddle_x - g / 2 * saddle_x**2 + h

        fig2.add_trace(
            go.Scatter(
                name='Saddle Point',
                x=[xy_maxima_x],
                y=[xy_maxima_y],
                textfont=dict(size=14),
                marker_symbol="x",
                marker=dict(size=8, color="salmon"),
                mode='markers+text',
            ))

        return fig1, fig2


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_7_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            vel = st.number_input("Initial Speed (m⋅s⁻¹)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        with col2:
            gravity = st.number_input("Gravity (m⋅s⁻²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        submitted = st.form_submit_button("Generate")

    try:
        fig1, fig2 = generate_task_7(u=vel, g=gravity, h=height)

        st.plotly_chart(fig1, **config.PLOTLY_CONFIG)
        st.plotly_chart(fig2, **config.PLOTLY_CONFIG)

    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    ##### Calculation of Projectile Range
    
    First, let us clarify the definition of the "range of projectile from starting point". This does **NOT** refer to the maximum horizontal distance ($x$ value when it lands), but the **shortest distance** between the projectile in one time-frame and the origin.
    For slightly better clarity, this type of range is denoted with a small caps $r$. This is illustrated in the diagram below, taken from the BPhO theory booklet. 
    """
    st.write("")
    with st.columns(3)[1]:
        st.image('./static/images/range.png')
    st.write("")
    r"""
    Recall that 
    
    $$
    \begin{equation}
        \begin{aligned}
            x &= ut\cos{\theta} \\  
            y &= ut\sin{\theta} - \frac{1}{2}gt^2
        \end{aligned}
    \end{equation}
    $$

    From Pythagoras, we also have that
    $$
    \begin{equation}
        r^2 = x^2 + y^2
    \end{equation}
    $$
    
    Therefore:
    $$
    \begin{align}
        r^2 &= u^2t^2\cos^2{\theta} + \left(ut\sin{\theta} - \frac{1}{2}gt^2\right)^2 \notag \\
        &= u^2t^2\cos^2{\theta} + u^2t^2\sin^2{\theta} - gt^2ut\sin{\theta} + \frac{1}{4}g^2t^4 \notag \\
        &= u^2t^2 - gt^3u\sin{\theta} + \frac{1}{4}g^2t^4\notag\\
    \end{align}
    $$
    
    $$
    \begin{equation}
        \therefore r = \sqrt{u^2t^2 - gt^3u\sin{\theta} + \frac{1}{4}g^2t^4}
    \end{equation}
    $$
    
    ##### Calculation of Minima and Maxima (For $r$ vs. $t$)
    
    We will conduct the following derivation, ignoring the trivial minimum at 0. Since the second derivative $\frac{\text{d}^2r}{\text{d}t^2} = 2r\frac{\text{d}^2r}{\text{d}t^2}$, therefore $\frac{\text{d}r}{\text{d}t} = 0$ if $\frac{\text{d}^2r}{\text{d}t^2} = 0$ as $r>0$. 
    
    $$
    \begin{equation}
        \frac{\text{d}^2r}{\text{d}t^2} = 2u^2t - 3gt^2u\sin{\theta} + g^2t^3
    \end{equation}
    $$
            
    Setting $\frac{\text{d}^2r}{\text{d}t^2} = 0$:
    $$
    \begin{align}
        0 &= 2u^2t - 3gt^2u\sin{\theta} + g^2t^3 \notag \\
        \Rightarrow0 &= t\left(2u^2 - 3gtu\sin{\theta} + g^2t^2\right)
    \end{align}
    $$
     
    Since $t>0$:
    $$
    \begin{align}
        0 &= 2u^2 - 3gtu\sin{\theta} + g^2t^2 \\
        \Rightarrow 0 &= t^2 - \frac{3u}{g}\sin{\theta}t + \frac{2u^2}{g^2} \notag \\
        \Rightarrow  0 &= \left(t-\frac{3u}{2g}\sin{\theta}\right)^2 - \frac{9u^2}{4g^2}\sin^2{\theta} + \frac{2u^2}{g^2}
    \end{align}
    $$
    
    By the quadratic formula:
    
    $$
    \begin{align*}
        t_\pm &= \frac{3u}{2g}\sin{\theta} \pm \sqrt{\frac{9u^2}{4g^2}\sin^2{\theta} - \frac{2u^2}{g^2}}\notag\\
         &= \frac{3u}{2g}\left(\sin{\theta} \pm \sqrt{\sin^2{\theta} - \frac{8}{9}}\right)
    \end{align*}
    $$
    
    
    Since we want real roots, therefore $\sin^2{\theta} > \frac{8}{9}$ or $\sin{\theta} > \frac{2\sqrt{2}}{3}$. Therefore, as $0\degree \leq \theta \leq 90\degree, \theta \gtrapprox 70.5$. At the critical angle, the saddle point occurs at:
    
    $$
    \begin{align}
        t_\pm &= \frac{3u}{2g}\sin{\theta}\notag\\
         &= \frac{3u}{2g} \cdot \frac{2\sqrt{2}}{3}\notag\\
         &= \frac{u}{g}\sqrt{2}
    \end{align}
    $$
    
    This is quite neat as it links to maximum horizontal range, $R_{\text{max}}$,  of a projectile fired from the ground ($\theta=45^\circ$) is:
    
    $$
    R_{\text{max}} = \frac{u}{g}
    $$
    """

st.divider()
