import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from cache import cache_data_default

st.set_page_config(page_title="Task 9", **config.page_config)
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

PLOT_DEFAULTS = {}

with code_tab, st.echo():

    @cache_data_default(**PLOT_DEFAULTS)
    def generate_task_9(*, kwarg):
        pass


# =====================
# MODEL
# =====================

with model_tab:
    with st.form("task_9_form"):
        "#### **Parameters**"

        col1, col2 = st.columns(2, gap="large")

        with col1:
            pass

        with col2:
            pass

        submitted = st.form_submit_button("Generate")

    try:
        # fig, *args = generate_task_9()

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

st.divider()
