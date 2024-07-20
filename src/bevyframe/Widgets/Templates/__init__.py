from bevyframe.Widgets.Templates.Containers import *
from bevyframe.Widgets.Templates.Inputs import *
from bevyframe.Widgets.Templates.Texts import *
from bevyframe.Widgets.Templates.Navbar import *
from bevyframe.Widgets.Templates.Media import *


class Icon(Widget):
    def __init__(self, i: str, **k):
        super().__init__('span', selector='material-symbols-rounded', innertext=i, **k)
