import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

st.set_page_config(page_title="Task 4", **config.page_config)

# ==================
r"""
## Task 4 - Maximize Projectile Range 

**Description:** Create a new projectile model which compares a trajectory to the trajectory which maximizes horizontal range given the same launch height and launch speed. Inputs are $u$, $h$, $g$ and $\theta$. For the maximum range trajectory you need to calculate the optimum angle. For $h > 0$ note this is not $45^\circ$...
"""

tab1, tab2, tab3 = st.tabs(["Model", "Derivations", "Source Code"])
