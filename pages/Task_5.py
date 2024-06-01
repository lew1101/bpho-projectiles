import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 5", **config.page_config)
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
