import streamlit as st

import config

st.set_page_config(page_title="Home", **config.page_config)
config.apply_custom_styles()

st.markdown(r"""

## BPhO Computational Challenge 2024 Submission

:orange[**Authors**: Kenneth Lew and Timothy Ka]

The British Physics Olympiad (BPhO) Computational Challenge is a  challenge running from Easter 2024 till August 2024 designed to test students' problem-solving abilities using computational methods. The deliverable of the challenge is to produce a screencast of maximum length two minutes which describes your response to the challenge. This year's computational challenge consists of a series of 9 progressively difficult tasks focused on the dynamics of projectiles. Further details about the challenge can be found [here](https://www.bpho.org.uk/bpho/computational-challenge/).

Our website is written entirely in Python using an open-source app framework named [**Streamlit**](https://streamlit.io/), which allows us to easily write interactive web apps quickly and easily. The embedded interactive charts are generated using [**Plotly**](https://plotly.com/python/), a powerful open-source data visualization library.

<hr style="width: 10%; margin: 35px 0 15px; padding: 0;"></hr>

[![Github](https://img.icons8.com/ios-glyphs/30/FFFFFF/github.png)](https://github.com/lew1101/bpho-projectiles)

""",
            unsafe_allow_html=True)
