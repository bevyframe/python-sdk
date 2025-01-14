from bevyframe.Widgets.Widget import Widget


class Image(Widget):
    def __init__(self, src: str, alt: str, **kwargs) -> None:
        super().__init__('img', src=src, alt=alt, **kwargs)
