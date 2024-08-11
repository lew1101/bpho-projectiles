import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 5", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 5 - Bounding Parabola

**Description:** Update your projectile model of a trajectory which passes through $(x, y)$ with the bounding parabola, in addition to minimum speed, max range and high and low ball curves. The bounding parabola marks the region where possible $(x, y)$ coordinates could be reached given $u$, $h$, $g$ inputs.

"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"target_x": 15.0, "target_y": 15.0, "g": 9.81, "u": 20.0, "h": 0.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_5(*, target_x: float, target_y: float, g: float, u: float, h: float):
        from math import sqrt, atan

        min_u = sqrt(g) * sqrt(target_y - h + sqrt(target_x**2 + (target_y - h)**2))
        # since only tan(theta) is used in the equation for the parabola, we can optimize by not taking atan and use value directly
        min_tan_theta = (target_y - h + sqrt(target_x**2 + (target_y - h)**2)) / target_x

        # min vel x values
        min_x = (min_tan_theta + sqrt(min_tan_theta**2 - 4 * (-h) * g *
                                      (1 + min_tan_theta**2) / 2 / min_u**2)) / 2 / (
                                          g * (1 + min_tan_theta**2) / 2 / min_u**2)
        min_x_traj = np.linspace(0, min_x, config.GRAPH_SAMPLES)

        # min vel trajectory
        min_y_traj = h + min_x_traj * min_tan_theta - min_x_traj**2 * g * (
            1 + min_tan_theta**2) / 2 / min_u**2

        # max range (used for both max range and bounding parabola calculation)
        max_x = u / g * sqrt(u**2 + 2 * g * h)
        bound_x = np.linspace(0, max_x, config.GRAPH_SAMPLES)

        # y values of the bounding parabola
        bound_parabola = u**2 / (2 * g) - g / (2 * u**2) * bound_x**2 + h

        # y values of the maximum range
        max_range_y = bound_x * (
            -h + sqrt(max_x**2 + h**2)) / max_x - bound_x**2 * sqrt(max_x**2 + h**2) / max_x**2 + h

        fig = go.Figure(
            data=[
                go.Scatter(name="Min. Velocity",
                           x=min_x_traj,
                           y=min_y_traj,
                           mode="lines",
                           line_shape='spline'),
                go.Scatter(name="Target",
                           x=[target_x],
                           y=[target_y],
                           text=[f"({target_x}, {target_y})"],
                           textposition="bottom center",
                           textfont=dict(size=15),
                           marker_symbol="x",
                           marker=dict(size=11),
                           mode='markers+text'),
                go.Scatter(name="Bounding Parabola",
                           x=bound_x,
                           y=bound_parabola,
                           mode="lines",
                           line_dash="longdash",
                           line_shape='spline'),
                go.Scatter(name="Max. Range",
                           x=bound_x,
                           y=max_range_y,
                           mode='lines',
                           line_dash="dashdot",
                           line_shape='spline')
            ],
            layout=config.GO_BASE_LAYOUT,
        )

        fig.update_layout(
            title_text="Hitting a Target",
            xaxis_title="x (m)",
            yaxis_title="y (m)",
        )

        if u > min_u:
            # find high and low ball trajectories
            a = g / 2 / u**2 * target_x**2
            b = -target_x
            c = target_y - h + g / 2 / u**2 * target_x**2

            # low ball
            low_tan_theta = (-b - sqrt(b**2 - 4 * a * c)) / 2 / a
            low_x = (low_tan_theta + sqrt(low_tan_theta**2 - 4 * (-h) * g *
                                          (1 + low_tan_theta**2) / 2 / u**2)) / 2 / (
                                              g * (1 + low_tan_theta**2) / 2 / u**2)
            low_x_list = np.linspace(0, low_x, config.GRAPH_SAMPLES)
            low_y_traj = h + low_x_list * low_tan_theta - low_x_list**2 * g * (
                1 + low_tan_theta**2) / 2 / u**2

            # high ball
            high_tan_theta = (-b + sqrt(b**2 - 4 * a * c)) / 2 / a
            high_x = (high_tan_theta + sqrt(high_tan_theta**2 + 4 * h * g *
                                            (1 + high_tan_theta**2) / 2 / u**2)) / 2 / (
                                                g * (1 + high_tan_theta**2) / 2 / u**2)
            high_x_list = np.linspace(0, high_x, config.GRAPH_SAMPLES)
            high_y_traj = h + high_x_list * high_tan_theta - high_x_list**2 * g * (
                1 + high_tan_theta**2) / 2 / u**2

            fig.add_traces(data=[
                go.Scatter(name="Low Ball",
                           x=low_x_list,
                           y=low_y_traj,
                           mode="lines",
                           line_dash="dot",
                           line_shape='spline'),
                go.Scatter(name="High Ball",
                           x=high_x_list,
                           y=high_y_traj,
                           mode="lines",
                           line_dash="dot",
                           line_shape='spline')
            ])

            return fig, min_u, atan(min_tan_theta), atan(low_tan_theta), atan(high_tan_theta)
        else:
            return fig, min_u, atan(min_tan_theta), None, None


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_5_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            x = st.number_input("Target X (m)", min_value=0.0, value=PLOT_DEFAULTS["target_x"])
            y = st.number_input("Target Y (m)", min_value=0.0, value=PLOT_DEFAULTS["target_y"])
            gravity = st.number_input("Gravity (m⋅s⁻²)", min_value=0.0, value=PLOT_DEFAULTS["g"])

        with col2:
            vel = st.number_input("Initial Speed (m⋅s⁻¹)", min_value=0.0, value=PLOT_DEFAULTS["u"])
            height = st.number_input("Height (m)", value=PLOT_DEFAULTS["h"])

        submitted = st.form_submit_button("Generate")

    try:
        results = generate_task_5(target_x=x, target_y=y, g=gravity, u=vel, h=height)
        fig, min_u, min_theta, low_theta, high_theta = results

        has_sufficient_vel = not (low_theta is None and high_theta is None)

        from math import degrees

        st.write("")
        if not has_sufficient_vel:
            st.warning("The input velocity (m⋅s⁻¹) is not sufficient to reach target.", icon="⚠️")
        f"""
        #### Calculated Values
        """

        if has_sufficient_vel:
            f"""
            **High Ball Launch Angle**: {degrees(high_theta):.2f} deg
            
            **Low Ball Launch Angle**: {degrees(low_theta):.2f} deg
            """
            st.write("")
        f"""
        **Minimum Initial Velocity**: {min_u:.2f} m⋅s⁻¹
        
        **Launch Angle of Minimum Velocity Trajectory**: {degrees(min_theta):.2f} deg
        """

        st.plotly_chart(fig, **config.PLOTLY_CONFIG)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    ##### Bounding Parabola Calculation
    
    The bounding parabola is defined as the region where possible (X,Y) coordinates could be reached given $u$,$h$,$g$ inputs, or in other words, the limit of the possible set of trajectories given a value of u.
    
    Recall that 
    $$
    \begin{equation}
        y = h + x\tan{\theta} + \frac{g}{2u^2}\sec^2{\theta}
    \end{equation}
    $$
    
    We can first simplify the equations by elimiating the h variable as shifting the y value by h at the end is equivalent. Hence:
    $$
    \begin{align*}
        y &= x\tan{\theta} + \frac{g}{2u^2}\sec^2{\theta}\\
        \Rightarrow 2u^2y &= 2u^2x\tan{\theta} - gx^2 - gx^2\tan^2{\theta}\\
        \Rightarrow 0 &= gx^2\tan^2{\theta} - 2u^2x\tan{\theta} + gx^2 + 2u^2y 
    \end{align*}
    $$
    
    As solutions only exist when discriminant is non-negative, hence:
    
    $$
    \begin{align*}
        4u^4x^2 - 4gx^2(2u^2y+gx^2) &\geq 0\\
        \frac{u^4}{g} &\leq 2u^2y + gx^2\\
        y &\leq frac{u^2}{2g} - frac{g}{2u^2}x^2
    \end{align*}
    $$
    
    Therefore, the bounding parabola is where:
    $$
    \begin{equation}
        y &= frac{u^2}{2g} - frac{g}{2u^2}x^2
    \end{equation}
    $$
    
    ##### Calculation for Projectile of Maxmimum Range
    
    Recall from task 4 that the maxmimum range is given by
    $$
    \begin{equation}
        R = frac{u^2}{g}\sqrt{1+frac{2gh}{u^2}}
    \end{equation}
    $$
    
    And from task 3 that minimum u parabola (with Y adjusted depending on u) is given by
    $$
    \begin{equation}
        y = x\left(\frac{Y + \sqrt{X^2 + (Y)^2}}{X}\right) + \left(\frac{\sqrt{X^2+(Y)^2}}{X^2}\right)x^2}
    \end{equation}
    $$
    
    It is trivial that trajectory of maximum range with an initial velocity $u$ corresponds with trajectory of minimum velocity to reach a point with (X,Y) = (max_x, 0). Therefore the above equation describes the trajectory of maximum range.
    
    ##### Extension of Projectile Trajectories
    
    Here, the problem to solve is to find the values of x where the projectile lands on the ground so the entire trajectory can be tracked.
    Referring back to task 2 for the equation of trajectory (ie equation 1 here):
    \[y = h + x\tan{\theta} + \frac{g}{2u^2}\sec^2{\theta}\]
    
    Using the same logic of equating y = 0 and to rearrange for x, we get:
    $$
    \begin{equation}
        x = \theta + \sqrt{\theta^2 + frac{4gh(1+\theta^2)}{2u^2}frac{1}{4u^2g(1+\theta^2)}
    \end{equation}
    $$
    
    And we have solved it!
    
    """

st.divider()
