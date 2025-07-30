from bevyframe.Widgets.Widget import Widget


class Container(Widget):
    def __init__(self, children: list, **kwargs,) -> None:
        super().__init__('div', children=children, **kwargs)


class Root(Container):
    def __init__(self, children: list, **kwargs) -> None:
        super().__init__(
            selector='root',
            id='root',
            children=children if isinstance(children, list) else [children],
            **kwargs
        )


class Box(Container):
    def __init__(self, children: list, onclick=None, **kwargs) -> None:
        super().__init__(
            selector='the_box',
            children=children if isinstance(children, list) else [children],
            onclick='' if onclick is None else onclick,
            **kwargs
        )


class Post(Container):
    def __init__(self, children: list, onclick=None, **kwargs) -> None:
        super().__init__(
            selector='post',
            children=children if isinstance(children, list) else [children],
            onclick=onclick if onclick else '',
            **kwargs
        )


class Line(Widget):
    def __init__(self, children: list, onclick=None, **kwargs) -> None:
        super().__init__(
            'p',
            children=children if isinstance(children, list) else [children],
            onclick=onclick if onclick else '',
            **kwargs
        )
