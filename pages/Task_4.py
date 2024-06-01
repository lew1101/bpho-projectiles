import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 4", **config.page_config)
config.apply_custom_styles()

# ==================
r"""
## Task 4 - Maximize Projectile Range 

**Description:** Create a new projectile model which compares a trajectory to the trajectory which maximizes horizontal range given the same launch height and launch speed. Inputs are $u$, $h$, $g$ and $\theta$. For the maximum range trajectory you need to calculate the optimum angle. For $h > 0$ note this is not $45^\circ$...
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
