from bevyframe.Widgets.Widget import Widget


class Container(Widget):
    def __init__(self, children: list = None, child = None, **kwargs,) -> None:
        super().__init__('div', children=children, child=child, **kwargs)


class Root(Container):
    def __init__(self, children: list, **kwargs) -> None:
        super().__init__(
            selector='root',
            id='root',
            children=children if isinstance(children, list) else [children],
            **kwargs
        )


class Box(Container):
    def __init__(self, children: list = None, child=None, innertext=None, onclick=None, selector=None, **kwargs) -> None:

        super().__init__(
            selector=f'the_box {selector}' if selector else 'the_box',
            children=children,
            child=child,
            innertext=innertext,
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
