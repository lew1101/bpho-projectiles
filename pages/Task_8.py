import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 8", **config.page_config)
config.apply_custom_styles()

# ==================
r"""
## Task 8 - Bouncing Projectile

**Description:** Use a numerical method assuming constant acceleration motion between small, discrete timesteps (e.g. the "Verlet" method) to compute a projectile trajectory which includes the possibility of a _bounce_. Define the _coefficient of restitution_ $C$ to be the vertical speed of separation divided by the vertical speed of approach. Assume a constant horizontal velocity, and stop the simulation after $N$ bounces. 

**_Extension_**: Modify your code to _animate_ the trajectory, and ideally, create a video file for efficient future playback.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_8(*, kwarg):
        pass


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_8_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            pass

        with col2:
            pass

        submitted = st.form_submit_button("Generate")

    try:
        # fig, *args = generate_task_8()

        st.write("")
        f"""
        #### Calculated Values

        """

        # st.plotly_chart(fig, **config.plotly_chart_config)
    except Exception as e:
        st.exception(e)

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """
