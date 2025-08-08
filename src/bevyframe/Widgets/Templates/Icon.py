from bevyframe.Widgets.Style import Size
from bevyframe.Widgets.Widget import Widget


class Icon(Widget):
    def __init__(self, i: str, size: int = 24, **k):
        super().__init__('span', selector='material-symbols-rounded', innertext=i, font_size=Size.pixel(size), **k)
