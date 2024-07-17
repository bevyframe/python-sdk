from bevyframe.Widgets.Widget import Widget

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
