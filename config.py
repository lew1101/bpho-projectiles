import streamlit as st

GRAPH_SAMPLES = 50

PAGE_CONFIG = dict(layout="wide", page_icon="static/favicon/favicon.ico")

PLOTLY_CONFIG = dict(use_container_width=True, displaylogo=False, include_mathjax="cdn")

GO_BASE_LAYOUT = dict(template="seaborn",
                      modebar_remove=["select", "lasso"],
                      autosize=True,
                      title=dict(font=dict(size=22, color="#FFBD45"), xanchor="left",
                                 pad=dict(l=0)),
                      xaxis=dict(ticks="outside",
                                 minor_ticks="outside",
                                 zeroline=True,
                                 zerolinecolor="silver",
                                 showgrid=True,
                                 showline=True),
                      yaxis=dict(ticks="outside",
                                 minor_ticks="outside",
                                 zeroline=True,
                                 zerolinecolor="silver",
                                 showgrid=True,
                                 showline=True))

custom_styles = r"""
<style>
h1, h2, h3, h4, h5, h6 {
    color: #ffbd45
}
[data-testid="stSidebarNav"] {
    background-image: url(app/static/favicon/favicon.png);
    background-position: top center;
    background-size: 110px;
    background-repeat: no-repeat;
    padding-top: 150px;
}
</style>
"""


@st.cache_resource
def apply_custom_styles() -> None:
    st.markdown(custom_styles, unsafe_allow_html=True)
