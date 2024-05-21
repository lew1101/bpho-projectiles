import plotly.graph_objects as go

custom_go_layout = go.Layout(modebar_remove=["select", "lasso"],
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
