from bevyframe.Widgets.Widget import Widget


class Container(Widget):
    def __init__(self, childs, **kwargs,):
        super().__init__('div', childs=childs, **kwargs)


class Root(Container):
    def __init__(self, childs, **kwargs):
        super().__init__(
            selector='root',
            childs=childs if isinstance(childs, list) else [childs],
            **kwargs
        )


class Box(Container):
    def __init__(self, childs, onclick=None, **kwargs):
        super().__init__(
            selector='the_box',
            childs=childs if isinstance(childs, list) else [childs],
            onclick='' if onclick is None else onclick,
            **kwargs
        )


class Post(Container):
    def __init__(self, childs, onclick=None, **kwargs):
        super().__init__(
            selector='post',
            childs=childs if isinstance(childs, list) else [childs],
            onclick=onclick if onclick else '',
            **kwargs
        )


class Line(Widget):
    def __init__(self, childs, onclick=None, **kwargs):
        super().__init__(
            'p',
            childs=childs if isinstance(childs, list) else [childs],
            onclick=onclick if onclick else '',
            **kwargs
        )
