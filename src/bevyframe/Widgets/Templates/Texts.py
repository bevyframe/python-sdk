from bevyframe.Widgets.Widget import Widget


class Label(Widget):
    def __init__(self, innertext: str, no_newline: bool = False, **kwargs) -> None:
        if no_newline:
            super().__init__('a', childs=[innertext], **kwargs)
        else:
            super().__init__('p', childs=[innertext], **kwargs)


class Bold(Widget):
    def __init__(self, innertext: str) -> None:
        super().__init__('b', innertext=innertext)


class Italic(Widget):
    def __init__(self, innertext: str) -> None:
        super().__init__('i', innertext=innertext)


class Link(Widget):
    def __init__(self, innertext: str, url: str, external: bool = False, selector: str = None, **kwargs) -> None:
        super().__init__(
            'a',
            innertext=innertext,
            href=url,
            selector=f'link {selector if selector else ""}',
            **({'target': '_blank'} if external else {}),
            **kwargs
        )


class Title(Widget):
    def __init__(self, innertext: str, **kwargs) -> None:
        super().__init__('h1', innertext=innertext, **kwargs)


class SubTitle(Widget):
    def __init__(self, innertext: str, **kwargs) -> None:
        super().__init__('h2', innertext=innertext, **kwargs)


class Heading(Widget):
    def __init__(self, innertext: str, **kwargs) -> None:
        super().__init__('h3', innertext=innertext, **kwargs)
