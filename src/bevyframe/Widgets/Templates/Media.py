from bevyframe.Widgets.Widget import Widget

Image = lambda src, alt, **kwargs: Widget(
    'img',
    src=src,
    alt=alt,
    **kwargs
)
