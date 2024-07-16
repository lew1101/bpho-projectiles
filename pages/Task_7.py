import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

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

PLOT_DEFAULTS = {"g": 9.81, "u": 10.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_7(*, u:float, g:float):
        from math import sqrt, sin, asin, degrees, radians, cos
        
        fig2 = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="xy Graph with stationary points plotted", xaxis_title="x (m)",  yaxis_title="y (m)")
            
        t = np.linspace(0,2.5,config.GRAPH_SAMPLES)
        angles = [30,45,60,70.5,78,85]
        range = []
        t_roots = []
        for theta in angles:
            theta_in_rad = radians(theta)
            indi_range = np.sqrt(u**2*t**2-g*t**3*u*sin(theta_in_rad)+g**2*t**4/4)
            range.append(indi_range)
            if theta>70.5:
                min_t = 3*u/2/g*(sin(theta_in_rad)-sqrt(sin(theta_in_rad)**2-8/9))
                max_t = 3*u/2/g*(sin(theta_in_rad)+sqrt(sin(theta_in_rad)**2-8/9))
                t_roots.append(min_t)
                t_roots.append(max_t)
             
            #Using what we did in task 2 for fig2
            ux = u * cos(theta_in_rad)
            uy = u * sin(theta_in_rad)

            total_t = uy *2 / g
            total_x = ux * total_t

            x = np.linspace(0, total_x, config.GRAPH_SAMPLES)
            y = (uy / ux) * x - (g / 2 / ux**2) * x**2
            fig2.add_trace(go.Scatter(name=f'angle: {theta} deg', x=x, y=y, mode="lines",  line_shape='spline'))
            

        fig1 = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Range VS Time", xaxis_title="t (s)",  yaxis_title="r (m)")
        
        for count, ranges in enumerate(range):
            fig1.add_trace(go.Scatter(name=f'angle: {angles[count]} deg', x=t, y=ranges, mode="lines", line_shape='spline'))
        
        for count, roots in enumerate(t_roots):
            if count == 1 or count == 0:
                theta_in_rad = radians(78)
            else:
                theta_in_rad = radians(85)
            root_range = sqrt(u**2*roots**2-g*roots**3*u*sin(theta_in_rad)+g**2*roots**4/4)
            if count%2 == 0:
                name = 'maxima'
            else:
                name = 'minima'
            fig1.add_trace(go.Scatter(name=name, x=[roots], y=[root_range],
                     textfont=dict(size=14), marker_symbol="x", marker=dict(size=8), mode='markers+text', showlegend=False))
        
        # Point of equality (ie having one saddle point instead of a maxima and minima)
        theta_in_rad = asin(2*sqrt(2)/3)
        saddle_root = u/g*sqrt(2)
        saddle_range = sqrt(u**2*saddle_root**2-g*saddle_root**3*u*sin(theta_in_rad)+g**2*saddle_root**4/4)
        fig1.add_trace(go.Scatter(name='saddle point', x=[saddle_root], y=[saddle_range],
                     textfont=dict(size=14), marker_symbol="x", marker=dict(size=8), mode='markers+text', showlegend=False))
        
        
        return fig1, fig2

        
        
        
    
    


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_7_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=PLOT_DEFAULTS["u"])

        with col2:
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        submitted = st.form_submit_button("Generate")

    try:
        fig1, fig2 = generate_task_7(u=vel, g=gravity)

        colA, colB = st.columns(2)
        
        with colA:
            st.plotly_chart(fig1, **config.PLOTLY_CONFIG)
        
        with colB:
            st.plotly_chart(fig2, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """

st.divider()
