from bevyframe.Widgets.Style import Size
from bevyframe.Widgets.Widget import Widget


class Icon:
    def __init__(self, i: str, size: int = 24, **k):
        self.icon_name = i
        self.size = size
        self.kwargs = k

    def bf_widget(self) -> list[str | dict | list]:
        return Widget(
            'span',
            selector='material-symbols-rounded',
            innertext=self.icon_name,
            font_size=Size.pixel(self.size),
            **self.kwargs
        ).bf_widget()
