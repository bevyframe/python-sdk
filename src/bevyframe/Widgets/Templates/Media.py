from bevyframe.Widgets.Widget import Widget


class Image:
    def __init__(self, src: str, alt: str, **kwargs) -> None:
        self.src = src
        self.alt = alt
        self.kwargs = kwargs

    def bf_widget(self) -> list[str | dict | list]:
        return Widget('img', src=self.src, alt=self.alt, **self.kwargs).bf_widget()
