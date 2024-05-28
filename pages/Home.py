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

[<img alt="Github" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIKc3R5bGU9ImZpbGw6I0ZGRkZGRjsiPgogICAgPHBhdGggZD0iTTEwLjksMi4xYy00LjYsMC41LTguMyw0LjItOC44LDguN2MtMC41LDQuNywyLjIsOC45LDYuMywxMC41QzguNywyMS40LDksMjEuMiw5LDIwLjh2LTEuNmMwLDAtMC40LDAuMS0wLjksMC4xIGMtMS40LDAtMi0xLjItMi4xLTEuOWMtMC4xLTAuNC0wLjMtMC43LTAuNi0xQzUuMSwxNi4zLDUsMTYuMyw1LDE2LjJDNSwxNiw1LjMsMTYsNS40LDE2YzAuNiwwLDEuMSwwLjcsMS4zLDFjMC41LDAuOCwxLjEsMSwxLjQsMSBjMC40LDAsMC43LTAuMSwwLjktMC4yYzAuMS0wLjcsMC40LTEuNCwxLTEuOGMtMi4zLTAuNS00LTEuOC00LTRjMC0xLjEsMC41LTIuMiwxLjItM0M3LjEsOC44LDcsOC4zLDcsNy42QzcsNy4yLDcsNi42LDcuMyw2IGMwLDAsMS40LDAsMi44LDEuM0MxMC42LDcuMSwxMS4zLDcsMTIsN3MxLjQsMC4xLDIsMC4zQzE1LjMsNiwxNi44LDYsMTYuOCw2QzE3LDYuNiwxNyw3LjIsMTcsNy42YzAsMC44LTAuMSwxLjItMC4yLDEuNCBjMC43LDAuOCwxLjIsMS44LDEuMiwzYzAsMi4yLTEuNywzLjUtNCw0YzAuNiwwLjUsMSwxLjQsMSwyLjN2Mi42YzAsMC4zLDAuMywwLjYsMC43LDAuNWMzLjctMS41LDYuMy01LjEsNi4zLTkuMyBDMjIsNi4xLDE2LjksMS40LDEwLjksMi4xeiI+PC9wYXRoPgo8L3N2Zz4="/>](https://github.com/lew1101/bpho-projectiles)

""",
            unsafe_allow_html=True)
