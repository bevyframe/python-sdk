from typing import Any

from bevyframe.Widgets.Widget import Widget


class Label(Widget):
    def __init__(self, innertext: str | Any, no_newline: bool = False, **kwargs) -> None:
        if no_newline:
            super().__init__('a', children=[str(innertext)], **kwargs)
        else:
            super().__init__('p', children=[str(innertext)], **kwargs)


class Bold(Widget):
    def __init__(self, innertext: str | Any) -> None:
        super().__init__('b', innertext=str(innertext))


class Italic(Widget):
    def __init__(self, innertext: str | Any) -> None:
        super().__init__('i', innertext=str(innertext))


class Link(Widget):
    def __init__(self, innertext: str | Any, url: str | Any, external: bool = False, selector: str | Any = None, **kwargs) -> None:
        super().__init__(
            'a',
            innertext=str(innertext),
            href=url,
            selector=f'link {selector if selector else ""}',
            **({'target': '_blank'} if external else {}),
            **kwargs
        )


class Title(Widget):
    def __init__(self, innertext: str | Any, **kwargs) -> None:
        super().__init__('h1', innertext=str(innertext), **kwargs)


class SubTitle(Widget):
    def __init__(self, innertext: str | Any, **kwargs) -> None:
        super().__init__('h2', innertext=str(innertext), **kwargs)


class Heading(Widget):
    def __init__(self, innertext: str | Any, **kwargs) -> None:
        super().__init__('h3', innertext=str(innertext), **kwargs)
