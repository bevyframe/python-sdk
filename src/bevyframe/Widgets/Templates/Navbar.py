from bevyframe.Widgets.Widget import Widget
from bevyframe.Widgets.Style import *


class Navbar(Widget):
    def __init__(self, children) -> None:
        super().__init__('nav', selector='Navbar', id='navbar', children=children)


class NavIcon(Widget):
    def __init__(self, src) -> None:
        super().__init__('a', selector='titleicon', children=[
            Widget(
                'img',
                src=src,
                height=Size.pixel(36),
                padding=Padding(bottom=Size.pixel(10)),
            )
        ])


class NavItem(Widget):
    def __init__(self, icon, link, alt, active=False) -> None:
        super().__init__('a', selector=('active' if active else 'inactive'), href=link, children=[
            Widget('button', children=[
                Widget(
                    'span',
                    selector='material-symbols-rounded',
                    innertext=icon,
                    alt=alt
                )
            ])
        ])
