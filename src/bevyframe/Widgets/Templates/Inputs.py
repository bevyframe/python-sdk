from bevyframe.Widgets.Widget import Widget
from bevyframe.Widgets.Style import *


class TextArea(Widget):
    def __init__(self, name, **kwargs):
        super().__init__('textarea', selector='textarea', id=name, name=name, **kwargs)


class Textbox(Widget):
    def __init__(self, name, selector='', **kwargs):
        super().__init__('input', selector=f'textbox {selector}', id=name, name=name, **kwargs)


class Button(Widget):
    def __init__(self, selector='', **kwargs):
        super().__init__('button', selector=f'button {selector}', **kwargs)


class Form(Widget):
    def __init__(self, method, childs):
        super().__init__('form', method=method, childs=childs)


class FAB(Widget):
    def __init__(self, onclick, **kwargs):
        super().__init__(
            'button',
            selector='button mini',
            position=Position.fixed(bottom=Size.pixel(20), right=Size.pixel(20)),
            width=Size.pixel(50),
            height=Size.pixel(50),
            onclick=onclick,
            **kwargs
        )
