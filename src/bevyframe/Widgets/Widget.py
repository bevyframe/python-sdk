from bevystyle.RenderCSS import RenderCSS
from bevyframe.Widgets.Style import Margin, Padding, Position, BorderRadius, Overflow
from bevystyle.Style import compile_style


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


def RenderHTML(tag, prop, ch) -> str:
    gen = f'<{tag}'
    for i in prop:
        if isinstance(prop[i], bool):
            gen += f' {i}'
        else:
            gen += f' {i}="' + str(prop[i]).replace('"', '\\"') + '"'
    if tag in no_content_elements:
        gen += ' />'
    else:
        gen += '>'
        for i in ch:
            gen += str(i)
        gen += f'</{tag}>'
    return gen


class Widget:
    def __init__(
            self,
            item,
            innertext: str = None,
            children: list = None,
            childs: list = None,
            child = None,
            style: dict = None,
            css: dict = None,
            color: str = None,
            background_color: str = None,
            background_image: str = None,
            aspect_ratio: str = None,
            height: str = None,
            width: str = None,
            min_height: str = None,
            max_height: str = None,
            min_width: str = None,
            max_width: str = None,
            text_align: str = None,
            visibility: str = None,
            margin: (str, Margin) = None,
            padding: (str, Padding) = None,
            opacity: float = None,
            position: (Position.fixed, Position.sticky, Position.absolute, Position.relative) = None,
            border_radius: str = None,
            border: str = None,
            font_size: str = None,
            vertical_align: str = None,
            cursor: str = None,
            text_decoration: str = None,
            onclick=None,
            onchange=None,
            assigned: str = None,
            **kwargs
    ):
        self.data = kwargs
        if onclick is not None:
            self.data['onclick'] = str(onclick)
        if onchange is not None:
            self.data['onchange'] = str(onchange)
        if assigned is not None:
            self.data['for'] = str(assigned)
        self.element = item
        self.style = {} if style is None else style
        self.content = []
        if style is None:
            self.style = compile_style(**locals())
        if innertext is not None:
            self.content = [innertext]
        elif children is not None:
            self.content = children
        elif child is not None:
            self.content = [child]
        elif childs is not None:
            self.content = childs
        elif item not in no_content_elements:
            self.content = []

    def bf_widget(self) -> list[str | dict | list]:
        prop = {}
        children = []
        if not self.style == {}:
            prop['style'] = RenderCSS(self.style)
        for i in self.data:
            if i == 'selector':
                prop['class'] = self.data[i]
            elif i in [
                'selected',
                'disabled',
                'checked'
            ]:
                if self.data[i]:
                    prop[i] = True
            else:
                prop[i] = self.data[i]
        if self.element not in no_content_elements:
            for i in self.content:
                if hasattr(i, 'bf_widget'):
                    children += [i.bf_widget()]
                else:
                    children += [i]
        return [self.element, prop, children]
