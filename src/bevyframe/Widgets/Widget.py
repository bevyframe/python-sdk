from bevyframe.Helpers.RenderCSS import RenderCSS
from bevyframe.Widgets.Style import Margin, Padding, Position
from bevyframe.Helpers.Exceptions import *
from bevyframe.Features.Style import compile_style


no_content_elements = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr"
]


class Widget:
    def __init__(
            self,
            item,
            innertext: str = None,
            childs: list = None,
            style: dict = None,
            css: dict = None,
            color: str = None,
            background_color: str = None,
            height: str = None,
            width: str = None,
            min_height: str = None,
            max_height: str = None,
            min_width: str = None,
            max_width: str = None,
            text_align: str = None,
            margin: (str, Margin) = None,
            padding: (str, Padding) = None,
            position: (Position.fixed, Position.sticky, Position.absolute, Position.relative) = None,
            border_radius: str = None,
            font_size: str = None,
            vertical_align: str = None,
            cursor: str = None,
            text_decoration: str = None,
            onclick=None,
            **kwargs
    ):
        self.data = kwargs
        if onclick is not None:
            self.data['onclick'] = str(onclick)
        self.element = item
        self.style = {} if style is None else style
        self.content = []
        if style is None:
            self.style = compile_style(**locals())
        if innertext is not None:
            self.content = [innertext]
        elif childs is not None:
            self.content = childs
        elif item not in no_content_elements:
            raise WidgetContentEmptyError('Widget content is empty')

    def render(self) -> str:
        gen = f'<{self.element}'
        if not self.style == {}:
            gen += f' style="{RenderCSS(self.style)}"'
        for i in self.data:
            if i == 'selector':
                gen += f' class="{self.data[i]}"'
            elif i in [
                'selected',
                'disabled',
                'checked'
            ]:
                if self.data[i]:
                    gen += f' {i}'
            else:
                gen += f' {i}="{self.data[i]}"'
        if self.element in no_content_elements:
            gen += '/>'
        else:
            gen += '>'
            for i in self.content:
                if hasattr(i, 'render'):
                    gen += i.render()
                else:
                    gen += str(i)
            gen += f'</{self.element}>'
        return gen
