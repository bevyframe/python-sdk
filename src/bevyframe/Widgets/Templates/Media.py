from bevyframe.Widgets.Widget import Widget


class Image(Widget):
    def __init__(self, src, alt, **kwargs):
        super().__init__('img', src=src, alt=alt, **kwargs)
