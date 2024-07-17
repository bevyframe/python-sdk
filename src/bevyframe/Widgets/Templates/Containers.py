from bevyframe.Widgets.Widget import Widget

Container = lambda childs, **kwargs: Widget(
    'div',
    childs=childs,
    **kwargs
)

Root = lambda childs, style = None, onclick = None: Container(
    selector='root',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else ''
)

Box = lambda childs, style = None, onclick = None: Container(
    selector='the_box',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else ''
)

Post = lambda childs, style = None, onclick = None: Container(
    selector='post',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else ''
)

Line = lambda childs, style = None, onclick = None, **kwargs: Widget(
    'p',
    childs=childs if isinstance(childs, list) else [childs],
    style=style if style else {},
    onclick=onclick if onclick else '',
    **kwargs
)
