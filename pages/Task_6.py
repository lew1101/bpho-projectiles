import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

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
