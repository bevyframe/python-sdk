from bevyframe.Helpers.RenderCSS import RenderCSS
from bevyframe.Widgets.Style import Margin, Padding, Position


class Widget:
    def __init__(
            self,
            item,
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
            position: Position = None,
            border_radius: str = None,
            font_size: str = None,
            vertical_align: str = None,
            **kwargs,
    ):
        self.data = {}
        self.element = item
        self.style = {} if style is None else style
        self.content = ''
        if style is None:
            if css is not None:
                self.style = css
            if isinstance(margin, str):
                self.style.update({'margin': margin})
            elif isinstance(margin, Margin):
                for i in ['top', 'right', 'bottom', 'left']:
                    if getattr(margin, i) is not None:
                        self.style.update({f'margin-{i}': getattr(margin, i)})
            if isinstance(padding, str):
                self.style.update({'padding': padding})
            elif isinstance(padding, Padding):
                for i in ['top', 'right', 'bottom', 'left']:
                    if getattr(padding, i) is not None:
                        self.style.update({f'padding-{i}': getattr(padding, i)})
            if position is not None:
                self.style.update({'position': position.item})
                for i in ['top', 'right', 'bottom', 'left']:
                    if getattr(position, i) is not None:
                        self.style.update({i: getattr(position, i)})
            k = [i for i in locals().keys()]
            for i in k:
                if i not in ['self', 'item', 'style', 'css', 'data', 'element', 'content', 'margin', 'padding', 'position', 'kwargs']:
                    if locals().get(i, None) is not None:
                        self.style.update({i.replace('_', '-'): locals()[i]})
        for arg in kwargs:
            if arg == 'innertext':
                self.content = [kwargs['innertext']]
            elif arg == 'childs':
                self.content = kwargs['childs']
            else:
                self.data.update({arg: kwargs[arg]})

    def render(self):
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
        if self.element in [
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
        ]:
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
