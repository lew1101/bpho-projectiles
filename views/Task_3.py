import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 3", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 3 - Hitting a Target 

**Description:** Create a new projectile model which is based upon calculating trajectories that are launched from $(0, h)$ and pass through a fixed position $(X, Y)$. Calculate the minimum launch speed to achieve this, and hence determine "low ball" and "high ball" trajectories.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {"target_x": 20.0, "target_y": 10.0, "g": 9.81, "u": 20.0, "h": 0.0}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_3(*, target_x: float, target_y: float, g: float, u: float, h: float):
        from math import sqrt, atan
        x = np.linspace(0, target_x, config.GRAPH_SAMPLES)

        min_u = sqrt(g) * sqrt(target_y - h + sqrt(target_x**2 + (target_y - h)**2))
        # since only tan(theta) is used in the equation for the parabola, we can optimize by not taking atan and use value directly
        min_tan_theta = (target_y - h + sqrt(target_x**2 + (target_y - h)**2)) / target_x

        # min vel trajectory
        min_y_traj = h + x * min_tan_theta - x**2 * g * (1 + min_tan_theta**2) / 2 / min_u**2

        fig = go.Figure(
            data=[
                go.Scatter(name="Min. vel.", x=x, y=min_y_traj, mode="lines", line_shape='spline'),
                go.Scatter(name="Target",
                           x=[target_x],
                           y=[target_y],
                           text=[f"({target_x}, {target_y})"],
                           textposition="bottom center",
                           textfont=dict(size=15),
                           marker_symbol="x",
                           marker=dict(size=11),
                           mode='markers+text')
            ],
            layout=config.GO_BASE_LAYOUT.update(title_text="Hitting a Target",
                                                xaxis_title="x (m)",
                                                yaxis_title="y (m)"),
        )

        if u > min_u:
            # find high and low ball trajectories
            a = g / 2 / u**2 * target_x**2
            b = -target_x
            c = target_y - h + g / 2 / u**2 * target_x**2

            # low ball
            low_tan_theta = (-b - sqrt(b**2 - 4 * a * c)) / 2 / a
            low_y_traj = h + x * low_tan_theta - x**2 * g * (1 + low_tan_theta**2) / 2 / u**2

            # high ball
            high_tan_theta = (-b + sqrt(b**2 - 4 * a * c)) / 2 / a
            high_y_traj = h + x * high_tan_theta - x**2 * g * (1 + high_tan_theta**2) / 2 / u**2

            fig.add_traces(data=[
                go.Scatter(name="Low ball",
                           x=x,
                           y=low_y_traj,
                           mode="lines",
                           line_dash="dot",
                           line_shape='spline'),
                go.Scatter(name="High ball",
                           x=x,
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
    with st.form("task_3_form"):
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
        results = generate_task_3(target_x=x, target_y=y, g=gravity, u=vel, h=height)
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
    ##### Finding the High Ball and Low Ball Trajectories
    
    Recall that the trajectory of the projectile is given by the function: 
    
    $$
    \begin{equation}
        y = h + x\tan{\theta} + \frac{g}{2u^2}\left(1+\tan^2{\theta}\right)x^2
    \end{equation}
    $$
    
    Let $(X, Y)$ represent the coordinates of the fixed target. Given that the initial launch velocity $u$ is known, valid launch angle(s) can be found using the equation 1:
    
    $$
        \begin{align}
        Y &= h + X\tan{\theta} + \frac{g}{2u^2}\left(1+\tan^2{\theta}\right)X^2 \notag \\
        \Rightarrow 0 &= \frac{g}{2u^2}X^2\tan^2{\theta} - X\tan{\theta} + Y - h + \frac{g}{2u^2}X^2
        \end{align}
    $$
    
    We can then solve for $\tan{\theta}$ using the quadratic formula, where:
    
    $$
    \begin{align*}
        a &= \frac{g}{2u^2}X^2 \\
        b &= -X \\ 
        c &= Y - h + \frac{g}{2u^2}X^2
    \end{align*}
    $$
    
    Thus:
    
    $$
    \begin{align*}
        \tan{\theta} &= \frac{-b \pm \sqrt{b^2-4ac}}{2a} \\
        &= \frac{-(-X) \pm \sqrt{(-X)^2-4\left(\frac{g}{2u^2}X^2\right)\left(Y - h + \frac{g}{2u^2}X^2\right)}}{2\frac{g}{2u^2}X^2} 
    \end{align*}
    $$
    
    Isolating for $\theta$:
    
    $$
    \begin{align}
        \Rightarrow \theta &= \tan^{-1}\left(\frac{X \pm \sqrt{X^2-\frac{2g}{u^2}X^2\left(Y - h + \frac{g}{2u^2}X^2\right)}}{\frac{g}{u^2}X^2}\right) \notag \\
        &= \boxed{\tan^{-1}\left(\frac{u^2 \pm u\sqrt{u^2-2g\left(Y - h + \frac{g}{2u^2}X^2\right)}}{gX}\right)}
    \end{align}
    $$
    
    The above equation can yield at most two solutions, given that the launch velocity is sufficient. The solution with the greater $\theta$ is considered the high ball trajectory, while the one with the smaller $\theta$ is the low ball trajectory.
    
    ##### Finding the Minimum Launch Trajectory
    
    By considering that the discriminant $b^2 - 4ac$ in equation 3 must be greater than zero to yield real solutions of $\theta$, the range of possible launch velocity $u$ (and consequently the minimum launch velocity) can be found.
    
    $$
    \begin{align*}
        X^2-4\left(\frac{gX^2}{2u^2}\right)\left(Y - h + \frac{gX^2}{2u^2}\right) &\geq 0\\
        \Rightarrow 1-\frac{2g}{u^2}\left(Y-h\right)-\frac{g^2X^2}{u^4} &\geq 0 \\
        \Rightarrow u^4-2gu^2(Y-h)-g^2X^2 &\geq 0
    \end{align*}
    $$
    
    Then, completing the square:
    
    $$
    \begin{gather*}
        \Rightarrow \left(u^2 - g(Y-h)\right)^2 - g^2(Y-h)^2 -g^2X^2 \geq 0 \\
        \Rightarrow \left(u^2 - g(Y-h)\right)^2 \geq g^2(Y-h)^2 + g^2X^2
    \end{gather*}
    $$

    Taking the square root on both sides:
    
    $$
    \begin{equation*}
        \Rightarrow u^2 - g(Y-h) \geq g\sqrt{X^2 + (Y-h)^2}
    \end{equation*}
    $$
    
    Note that only the principal root is taken, because $u$ must be real and positive. 
    
    $$
    \begin{align}
        \Rightarrow u^2 &\geq g\left((Y-h) + \sqrt{X^2 + (Y-h)^2}\right) \notag \\
        \Rightarrow u &\geq \boxed{\sqrt{g}\sqrt{(Y-h) + \sqrt{X^2 + (Y-h)^2}}}
    \end{align}
    $$
    
    The launch angle of the minimum $u$ trajectory can be found by replacing the minimum solution for $u$ in equation 2 for $u$. Recognizing that $b^2-4ac=0$ for the minimum velocity $u$:
    
    $$
    \begin{align}
            \tan{\theta} &= \frac{-b}{2a} \notag \\
            &= \frac{X}{\frac{g}{u^2}X^2} \notag \\
            &= \frac{u^2}{gX} \notag \\
            &= \frac{(Y-h) + \sqrt{X^2 + (Y-h)^2}}{X}
    \end{align}
    $$
    $$
    \begin{equation}
        \therefore \theta = \boxed{\tan^{-1}{\frac{(Y-h) + \sqrt{X^2 + (Y-h)^2}}{X}}}
    \end{equation}
    $$
    
    Replacing for $\tan{\theta}$ in equation 1, we can find the equation of the minimum $u$ trajectory:
    
    $$
    \begin{align}
        y &= h + x\tan{\theta} + \frac{g}{2u^2}\left(1+\tan^2{\theta}\right)x^2 \notag \\
        &= h + x\left(\frac{Y - h + \sqrt{X^2 + (Y-h)^2}}{X}\right) + \frac{g}{2g\left(Y - h + \sqrt{X^2 + (Y-h)^2}\right)}\left(1+\frac{\left(Y - h + \sqrt{X^2 + (Y-h)^2}\right)^2}{X^2}\right)x^2 \notag \\
        &= h + x\left(\frac{Y - h + \sqrt{X^2 + (Y-h)^2}}{X}\right) + \frac{1}{2\left(Y - h + \sqrt{X^2 + (Y-h)^2}\right)}\left(\frac{X^2 + (Y-h)^2 + 2(Y-h)\sqrt{X^2+(Y-h)^2} + X^2 + (Y-h)^2}{X^2}\right)x^2 \notag \\
        &= h + x\left(\frac{Y - h + \sqrt{X^2 + (Y-h)^2}}{X}\right) + \frac{\sqrt{X^2 + (Y-h)^2}}{Y - h + \sqrt{X^2 + (Y-h)^2}}\left(\frac{Y - h + \sqrt{X^2+(Y-h)^2}}{X^2}\right)x^2 \notag \\
        &= \boxed{h + x\left(\frac{Y - h + \sqrt{X^2 + (Y-h)^2}}{X}\right) + \left(\frac{\sqrt{X^2+(Y-h)^2}}{X^2}\right)x^2} \\
    \end{align}
    $$
    
    
    """

st.divider()
