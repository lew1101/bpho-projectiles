import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 9", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 9 - Air Resistance

**Description:** Write a new projectile model which compares a drag-free model (use what you have already done in previous challenges) with a model incorporating the effect of air resistance. Use a _Verlet_ method to solve the air-resistance case with a $v^2$ drag dependence. It is possible to solve motion under drag which varies with the square of velocity analytically in 1D (see [here](http://www.eclecticon.info/index_htm_files/Mechanics%20-%20Modelling%20air%20resistance.pdf)) but in 2D projectile motion drag always opposes the velocity vector, which makes the maths much harder. So write a numerical recipe instead.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {
    "theta": 30.0,
    "g": 9.81,
    "u": 20.0,
    "h": 2.0,
    'Cd': 1.0,
    'a': 0.007854,
    'P': 1.0,
    'm': 0.1,
    "dt": 0.01
}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_9(*, theta: float, u: float, h: float, g: float, Cd: float, a: float,
                        P: float, m: float, dt: float):
        from math import sqrt, sin, cos, radians

        y_x = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Projectile Motion Model", xaxis_title="x (m)",  yaxis_title="y (m)")
        y_t = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Y Position vs. Time", xaxis_title="t (s)",  yaxis_title="y (m)")
        vx_t = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="X Velocity vs. Time", xaxis_title="t (s)",  yaxis_title="vx (ms⁻¹)")
        vy_t = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Y Velocity vs Time", xaxis_title="t (s)",  yaxis_title="vy (ms⁻¹)")
        v_t = go.Figure(layout=config.GO_BASE)\
            .update_layout(title_text="Velocity vs. Time", xaxis_title="t (s)",  yaxis_title="v (ms⁻¹)")

        rad = radians(theta)

        ux = u * cos(rad)
        uy = u * sin(rad)

        #Drag Free Model As in Task 2

        drag_free_apogee_x = ux * uy / g
        drag_free_apogee_y = h + (uy**2) / 2 / g

        total_t = (uy + sqrt(uy**2 + 2 * g * h)) / g
        drag_free_t = np.linspace(0, total_t, config.GRAPH_SAMPLES)

        drag_free_x = ux * drag_free_t
        drag_free_y = h + uy * drag_free_t - g * drag_free_t**2 / 2
        drag_free_vx = np.ones(config.GRAPH_SAMPLES) * ux
        drag_free_vy = uy - g * drag_free_t
        drag_free_v = np.sqrt(drag_free_vx**2 + drag_free_vy**2)

        y_x.add_trace(go.Scatter(name="Drag Free", x=drag_free_x, y=drag_free_y, mode="lines",  line_shape='spline'))\
            .add_trace(go.Scatter(name="Drag Free Apogee", x=[drag_free_apogee_x], y=[drag_free_apogee_y], text=[f"({drag_free_apogee_x:.2f}, {drag_free_apogee_y:.2f})"],
                    textposition="bottom center", textfont=dict(size=14), marker_symbol="0", marker=dict(size=8), mode='markers+text'))\
            .add_trace(go.Scatter(name="Drag Free Range", x=[drag_free_x[-1]], y=[0], text=[f"({drag_free_x[-1]:.2f}, {0})"],
                    textposition="top center", textfont=dict(size=14), marker_symbol="x", marker=dict(size=11), mode='markers+text', showlegend = False))

        y_t.add_trace(
            go.Scatter(name="Drag Free",
                       x=drag_free_t,
                       y=drag_free_y,
                       mode="lines",
                       line_shape='spline'))

        vx_t.add_trace(
            go.Scatter(name="Drag Free",
                       x=drag_free_t,
                       y=drag_free_vx,
                       mode="lines",
                       line_shape='spline'))

        vy_t.add_trace(
            go.Scatter(name="Drag Free",
                       x=drag_free_t,
                       y=drag_free_vy,
                       mode="lines",
                       line_shape='spline'))

        v_t.add_trace(
            go.Scatter(name="Drag Free",
                       x=drag_free_t,
                       y=drag_free_v,
                       mode="lines",
                       line_shape='spline'))

        #Resistance Included Model Using Verlet Method

        k = Cd * P * a / m / 2

        total_t_drag = 0

        current_x = 0
        current_y = h

        current_v = u
        current_vx = ux
        current_vy = uy

        drag_t = []
        drag_x = []
        drag_y = []
        drag_vx = []
        drag_vy = []
        drag_v = []

        while current_y > 0:
            drag_t.append(total_t_drag)
            drag_x.append(current_x)
            drag_y.append(current_y)
            drag_vx.append(current_vx)
            drag_vy.append(current_vy)
            drag_v.append(current_v)

            ax = -current_vx * current_v * k
            ay = -g - current_vx * current_v * k
            current_x += current_vx * dt + ax * dt**2 / 2
            current_y += current_vy * dt + ay * dt**2 / 2
            current_vx += ax * dt
            current_vy += ay * dt
            current_v = sqrt(current_vx**2 + current_vy**2)

            total_t_drag += dt

        #exact apogee calculation not possible as graph plotted using verlet method

        y_x.add_trace(go.Scatter(name="Drag Included", x=drag_x, y=drag_y, mode="lines",  line_shape='spline'))\
            .add_trace(go.Scatter(name="Drag Included Range", x=[drag_x[-1]], y=[0], text=[f"({drag_x[-1]:.2f}, {0})"],
                    textposition="top center", textfont=dict(size=14), marker_symbol="x", marker=dict(size=11), mode='markers+text', showlegend = False))

        y_t.add_trace(
            go.Scatter(name="Drag Included", x=drag_t, y=drag_y, mode="lines", line_shape='spline'))

        vx_t.add_trace(
            go.Scatter(name="Drag Included", x=drag_t, y=drag_vx, mode="lines",
                       line_shape='spline'))

        vy_t.add_trace(
            go.Scatter(name="Drag Included", x=drag_t, y=drag_vy, mode="lines",
                       line_shape='spline'))

        v_t.add_trace(
            go.Scatter(name="Drag Included", x=drag_t, y=drag_v, mode="lines", line_shape='spline'))

        return y_x, y_t, vx_t, vy_t, v_t, total_t, total_t_drag, k


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_9_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2)

        with col1:
            theta = st.number_input("Launch Angle (deg)",
                                    min_value=0.0,
                                    max_value=90.0,
                                    value=PLOT_DEFAULTS["theta"])
            vel = st.number_input("Initial Speed (m/s)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])
            gravity = st.number_input("Gravity (m/s²)", min_value=0.0, value=PLOT_DEFAULTS["g"])
            time_step = st.number_input("Time Step (s)",
                                        min_value=0.001,
                                        step=0.001,
                                        value=PLOT_DEFAULTS["dt"],
                                        format="%.3f")

        with col2:
            Cd = st.number_input("Drag Coefficient Cd",
                                 min_value=0.001,
                                 step=0.001,
                                 value=PLOT_DEFAULTS["Cd"],
                                 format="%.3f")
            area = st.number_input("Cross Sectional Area (m²)",
                                   min_value=0.001,
                                   step=0.001,
                                   value=PLOT_DEFAULTS["a"],
                                   format="%.3f")
            density = st.number_input("Air Density (kgm⁻³)",
                                      min_value=0.001,
                                      step=0.001,
                                      value=PLOT_DEFAULTS["P"],
                                      format="%.3f")
            mass = st.number_input("Object Mass (m)",
                                   min_value=0.001,
                                   step=0.001,
                                   value=PLOT_DEFAULTS["m"],
                                   format="%.3f")

        submitted = st.form_submit_button("Generate")

    try:
        y_x, y_t, vx_t, vy_t, v_t, total_t, total_t_drag, k = generate_task_9(theta=theta,
                                                                              u=vel,
                                                                              h=height,
                                                                              g=gravity,
                                                                              Cd=Cd,
                                                                              a=area,
                                                                              P=density,
                                                                              m=mass,
                                                                              dt=time_step)
        f"""
        #### Calculated Values
        
        **Flight Time (Without Drag)**: {total_t:.3f} s
        
        **Flight Time (With Drag)**: {total_t_drag:.3f} s
        
        **Air Resistance Factor**: {k:.3f}
        """

        st.plotly_chart(y_x, **config.PLOTLY_CONFIG)

        col_a, col_b = st.columns(2)

        with col_a:
            st.plotly_chart(y_t, **config.PLOTLY_CONFIG)
            st.plotly_chart(vx_t, **config.PLOTLY_CONFIG)

        with col_b:
            st.plotly_chart(v_t, **config.PLOTLY_CONFIG)
            st.plotly_chart(vy_t, **config.PLOTLY_CONFIG)

    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """

st.divider()
