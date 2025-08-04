from bevyframe.Widgets.Templates.Containers import *
from bevyframe.Widgets.Templates.Inputs import *
from bevyframe.Widgets.Templates.Texts import *
from bevyframe.Widgets.Templates.Navbar import *
from bevyframe.Widgets.Templates.Media import *
from bevyframe.Widgets.Templates.Specialized.TabView import TabView, Tab
from bevyframe.Widgets.Templates.Specialized.DualContainer import DualContainer


class Icon(Widget):
    def __init__(self, i: str, size: int = 24, **k):
        super().__init__('span', selector='material-symbols-rounded', innertext=i, font_size=Size.pixel(size), **k)
