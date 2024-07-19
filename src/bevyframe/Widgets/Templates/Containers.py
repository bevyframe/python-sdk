from bevyframe.Widgets.Widget import Widget

Container = lambda childs, **kwargs: Widget(
    'div',
    childs=childs,
    **kwargs
)

Root = lambda childs, style = None, **kwargs: Container(
    selector='root',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    **kwargs
)

Box = lambda childs, style = None, onclick = None, **kwargs: Container(
    selector='the_box',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else '',
    **kwargs
)

Post = lambda childs, style = None, onclick = None, **kwargs: Container(
    selector='post',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else '',
    **kwargs
)

Line = lambda childs, style = None, onclick = None, **kwargs: Widget(
    'p',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else '',
    **kwargs
)
