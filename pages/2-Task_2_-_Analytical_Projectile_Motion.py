import streamlit as st

import plotly.express as px
import numpy as np

from helpers.plotly_helpers import apply_custom_plotly_settings

st.set_page_config(page_title="Task 2", layout="wide")

# ==================
r"""
## Task 2 - Analytical Projectile Motion  

**Description:** Create a more sophisticated exact ("analytical") model using equations for the projectile trajectory. In this case define a equally spaced _array_ of $x$ coordinate values between 0 and the maximum horizontal range, $R$. Plot the trajectory and the apogee.
"""

tab1, tab2 = st.tabs(["Model", "Derivation"])

# ==================
# MODEL
# ==================

with tab1:
    body = st.empty()

    with st.expander("See Source Code"), st.echo():

        # @apply_custom_plotly_settings
        def generate_task_2(theta: float, g: float, u: float, h: float, steps: int):
            from math import sin, cos, sqrt, radians

            pass

    with body.container():
        with st.form("task_1_form"):
            "#### **Parameters**"

            col1, col2 = st.columns(2, gap="large")

            with col1:
                theta = st.number_input("Angle (deg)",
                                        min_value=0.0,
                                        max_value=90.0,
                                        value=45.0,
                                        key="theta")
                gravity = st.number_input("Angle (m/s²)", min_value=0.0, value=9.81, key="gravity")
                steps = st.number_input("Time Intervals (s)", min_value=0, value=1, key="dt")

            with col2:
                vel = st.number_input("Initial Velocity (m/s)",
                                      min_value=0.0,
                                      value=20.0,
                                      key="vel")
                height = st.number_input("Height (m)", value=2.0, key="height")

            submitted = st.form_submit_button("Generate")

        try:
            fig = generate_task_2(theta, gravity, vel, height, dt)
            # st.plotly_chart(fig, config={"displaylogo": False})
        except Exception as e:
            st.exception(e)

# ==================
# DERVIATIONS
# ==================

with tab2:
    r"""
    """
