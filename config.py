import streamlit as st
import plotly.graph_objects as go

page_config = dict(layout="wide", page_icon="static/favicon/favicon.ico")

plotly_chart_config = dict(use_container_width=True, displaylogo=False)

custom_go_layout = go.Layout(template="seaborn",
                             modebar_remove=["select", "lasso"],
                             title=dict(font=dict(size=22, color="#FFBD45"),
                                        xanchor="left",
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
h1, h2, h3, h4, h5 {
    color: #ffbd45
}
[data-testid="stSidebarNav"] {
    background-image: url(app/static/favicon/favicon.png);
    background-position: top center;
    background-size: 110px;
    background-repeat: no-repeat;
    padding-top: 120px;
}
</style>
"""


@st.cache_resource
def apply_custom_styles() -> None:
    st.markdown(custom_styles, unsafe_allow_html=True)
