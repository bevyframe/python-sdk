from bevyframe.Widgets.Templates import Container
from bevyframe.Widgets.Widget import Widget
from bevyframe.Widgets.Style import *


class TextArea(Widget):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__('textarea', selector='textarea', id=name, name=name, **kwargs)


class Textbox:
    def __init__(self, name: str, selector='', label=None, **kwargs) -> None:
        self.name = name
        self.selector = selector
        self.label = label
        self.kwargs = kwargs

    def bf_widget(self) -> list[str | dict | list]:
        if self.label is None:
            return Widget(
                'input',
                selector=f'textbox {self.selector}',
                id=self.name,
                name=self.name,
                **self.kwargs
            ).bf_widget()
        return Widget(
            'label',
            children=[
                Widget(
                    'p',
                    innertext=self.label,
                    margin=Margin(
                        bottom=Size.pixel(0),
                        left=Size.pixel(3),
                    ),
                    text_align=Align.left
                ) if self.label else "",
                Widget('input', selector=f'textbox {self.selector}', id = self.name, name = self.name, **self.kwargs)
            ]
        ).bf_widget()


class TextboxTypes:
    text = 'text'
    password = 'password'
    email = 'email'
    number = 'number'
    tel = 'tel'
    url = 'url'
    search = 'search'
    date = 'date'
    datetime_local = 'datetime-local'
    month = 'month'
    time = 'time'
    week = 'week'


class Selection(Widget):
    def __init__(self, name: str, selected: str, options: list[str], label: str, selector='', **kwargs) -> None:
        children = [
            Widget('option', innertext=i, selected=i == selected, value=i)
            for i in options
        ]
        super().__init__(
            'label',
            children=[
                Widget(
                    'p',
                    innertext=label,
                    margin=Margin(
                        bottom=Size.pixel(0),
                        left=Size.pixel(3),
                    ),
                    text_align=Align.left
                ) if label else "",
                Container(
                    selector=f"textbox {selector}",
                    children=[
                        Widget(
                            'select',
                            selector=f"textbox {selector}",
                            id=name,
                            name=name,
                            children=children,
                            background_color=Color.transparent
                        ),
                    ]
                )
            ]
        )


class Button(Widget):
    def __init__(self, selector: str = '', **kwargs) -> None:
        super().__init__('button', selector=f'button {selector}', **kwargs)


class Form:
    def __init__(self, method: str, children: list = None, child=None, action: str = None) -> None:
        self.method = method
        self.children = [child] if child else children
        self.action = action if action else ''

    def bf_widget(self) -> list[str | dict | list]:
        if self.action:
            return Widget('form', method=self.method, children=self.children, action=self.action).bf_widget()
        else:
            return Widget('form', method=self.method, children=self.children).bf_widget()


class Method:
    post = 'POST'
    get = 'GET'
    put = 'PUT'
    delete = 'DELETE'
    patch = 'PATCH'



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
