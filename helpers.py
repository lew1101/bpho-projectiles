def apply_custom_plotly_settings(gen):

    def inner(*args, **kwargs):
        return gen(*args, **kwargs) \
            .update_layout(modebar_remove=["select", "lasso"]) \
            .update_xaxes(ticks="outside",
                         minor_ticks="outside",
                         zeroline=True,
                         zerolinecolor='silver',
                         showgrid=True,
                         showline=True) \
            .update_yaxes(ticks="outside",
                         minor_ticks="outside",
                         zeroline=True,
                         zerolinecolor='silver',
                         showgrid=True,
                         showline=True)

    return inner
