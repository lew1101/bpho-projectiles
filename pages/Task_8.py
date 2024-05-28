import streamlit as st

import plotly.graph_objects as go
import numpy as np

import config

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
