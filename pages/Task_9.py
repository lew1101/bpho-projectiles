import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

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

with code_tab, st.echo():
    pass

# =====================
# MODEL
# =====================

with model_tab:
    pass

# =====================
# DERIVATION
# =====================

with math_tab:
    r"""
    """
