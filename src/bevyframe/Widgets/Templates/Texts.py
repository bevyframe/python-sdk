from bevyframe.Widgets.Widget import Widget


class Label(Widget):
    def __init__(self, innertext, no_newline=False, **kwargs):
        if no_newline:
            super().__init__('a', childs=[innertext], **kwargs)
        else:
            super().__init__('p', childs=[innertext], **kwargs)


class Bold(Widget):
    def __init__(self, innertext):
        super().__init__('b', innertext=innertext)


class Italic(Widget):
    def __init__(self, innertext):
        super().__init__('i', innertext=innertext)


class Link(Widget):
    def __init__(self, innertext, url, external=False, selector=None, **kwargs):
        super().__init__(
            'a',
            innertext=innertext,
            href=url,
            selector=f'link {selector if selector else ""}',
            **({'target': '_blank'} if external else {}),
            **kwargs
        )


class Title(Widget):
    def __init__(self, innertext, **kwargs):
        super().__init__('h1', innertext=innertext, **kwargs)


class SubTitle(Widget):
    def __init__(self, innertext, **kwargs):
        super().__init__('h2', innertext=innertext, **kwargs)


class Heading(Widget):
    def __init__(self, innertext, **kwargs):
        super().__init__('h3', innertext=innertext, **kwargs)
