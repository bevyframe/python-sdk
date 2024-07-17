from bevyframe.Widgets.Templates.Containers import *
from bevyframe.Widgets.Templates.Inputs import *
from bevyframe.Widgets.Templates.Texts import *
from bevyframe.Widgets.Templates.Navbar import *
from bevyframe.Widgets.Templates.Media import *

Icon = lambda i, **k: Widget('span', selector='material-symbols-rounded', innertext=i, **k)
