import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 5", **config.PAGE_CONFIG)
config.apply_custom_styles()

# ==================
r"""
## Task 5 - Bounding Parabola

**Description:** Update your projectile model of a trajectory which passes through $(x, y)$ with the _bounding parabola_, in addition to minimum speed, max range and high and low ball curves. The bounding parabola marks the region where possible $(x, y)$ coordinates could be reached given $u$, $h$, $g$ inputs.
"""

model_tab, math_tab, code_tab, = st.tabs(["Model", "Derivations", "Source Code"])

# =====================
# CODE
# =====================

PLOT_DEFAULTS = {}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_5(*, kwarg):
        pass


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_5_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            pass

        with col2:
            pass

        submitted = st.form_submit_button("Generate")

    try:
        # fig, *args = generate_task_5()
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

st.divider()
