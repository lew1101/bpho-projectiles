import plotly.graph_objects as go

page_config = dict(layout="wide", page_icon="res/favicon/favicon.ico")

plotly_chart_config = dict(displaylog=False)

go_layout = go.Layout(modebar_remove=["select", "lasso"],
                             xaxis=dict(ticks="outside",
                                        minor_ticks="outside",
                                        zeroline=True,
                                        zerolinecolor='silver',
                                        showgrid=True,
                                        showline=True),
                             yaxis=dict(ticks="outside",
                                        minor_ticks="outside",
                                        zeroline=True,
                                        zerolinecolor='silver',
                                        showgrid=True,
                                        showline=True))



