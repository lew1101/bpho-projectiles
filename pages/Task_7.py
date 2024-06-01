import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config
from utils import cache_data_default

st.set_page_config(page_title="Task 7", **config.page_config)
config.apply_custom_styles()

# ==================
r"""
## Task 7 - Range of Projectile vs. Time

**Description:** A curious fact is that the range $R$ of a projectile from the launch point, plotted against time $t$ can, for launch angles greater than about $70.5^\circ$, actually pass through a _local maximum and then a minimum_, before increasing with increasing gradient. Use the derivations to recreate the graphs of $R$ vs $t$. Work out the times, $x$, $y$, and $r$ values for these maxima and minima and plot these via a suitable marker.
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
