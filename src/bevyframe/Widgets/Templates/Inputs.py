from bevyframe.Widgets.Widget import Widget
from bevyframe.Widgets.Style import *

TextArea = lambda name, **kwargs: Widget(
    'textarea',
    selector='textarea',
    id=name,
    name=name,
    **kwargs
)

Textbox = lambda name, selector = '', **kwargs: Widget(
    'input',
    name=name,
    id=name,
    selector=f'textbox {selector}',
    **kwargs
)

Button = lambda selector = '', **kwargs: Widget(
    'button',
    selector=f'button {selector}',
    **kwargs
)

Form = lambda method, childs: Widget(
    'form',
    method=method,
    childs=childs
)

FAB = lambda onclick, **kwargs: Widget(
    'button',
    selector=f'button mini',
    position=Position.fixed(bottom=Size.pixel(20), right=Size.pixel(20)),
    width=Size.pixel(50),
    height=Size.pixel(50),
    onclick=onclick,
    **kwargs
)
