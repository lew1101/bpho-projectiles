import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 6", **config.page_config)
config.apply_custom_styles()

# ==================
r"""
## Task 6 - Arc Length of Projectile Motion

**Description:** Now update your projectile model with a calculation of the _distance travelled_ by the projectile i.e. the length of the inverted parabolic arc. This can be computed exactly!
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_6(*, kwarg):
        pass


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_6_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            pass

        with col2:
            pass

        submitted = st.form_submit_button("Generate")

    try:
        # fig, *args = generate_task_6()

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
