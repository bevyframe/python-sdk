from bevyframe.Widgets.Widget import Widget
from bevyframe.Widgets.Style import *


class Navbar(Widget):
    def __init__(self, childs):
        super().__init__('nav', selector='Navbar', id='navbar', childs=childs)


class NavIcon(Widget):
    def __init__(self, src):
        super().__init__('a', selector='titleicon', childs=[
            Widget(
                'img',
                src=src,
                height=Size.pixel(36),
                padding=Padding(bottom=Size.pixel(10)),
            )
        ])


class NavItem(Widget):
    def __init__(self, icon, link, alt, active=False):
        super().__init__('a', selector=('active' if active else 'inactive'), href=link, childs=[
            Widget('button', childs=[
                Widget(
                    'span',
                    selector='material-symbols-rounded',
                    innertext=icon,
                    alt=alt
                )
            ])
        ])
