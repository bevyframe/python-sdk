from bevyframe.Widgets.Widget import Widget
from bevyframe.Widgets.Style import *


class TextArea(Widget):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__('textarea', selector='textarea', id=name, name=name, **kwargs)


class Textbox(Widget):
    def __init__(self, name: str, selector='', **kwargs) -> None:
        super().__init__('input', selector=f'textbox {selector}', id=name, name=name, **kwargs)


class Selection(Widget):
    def __init__(self, name: str, selected: str, options: list[str], selector='', **kwargs) -> None:
        childs = [
            Widget('option', innertext=i, selected=i == selected, value=i)
            for i in options
        ]
        super().__init__('select', selector=f'textbox {selector}', id=name, name=name, childs=childs, **kwargs)


class Button(Widget):
    def __init__(self, selector: str = '', **kwargs) -> None:
        super().__init__('button', selector=f'button {selector}', **kwargs)


class Form(Widget):
    def __init__(self, method: str, childs: list) -> None:
        super().__init__('form', method=method, childs=childs)


class FAB(Widget):
    def __init__(self, onclick: any, **kwargs) -> None:
        super().__init__(
            'button',
            selector='button mini',
            position=Position.fixed(bottom=Size.pixel(20), right=Size.pixel(20)),
            width=Size.pixel(50),
            height=Size.pixel(50),
            onclick=onclick,
            **kwargs
        )
