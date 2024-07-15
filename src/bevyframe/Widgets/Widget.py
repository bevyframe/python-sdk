from bevyframe.Helpers.RenderCSS import RenderCSS


class Widget:
    def __init__(self, item, **kwargs):
        self.data = {}
        self.element = item
        self.style = {}
        for arg in kwargs:
            if arg == 'innertext':
                self.content = [kwargs['innertext']]
            elif arg == 'childs':
                self.content = kwargs['childs']
            elif arg == 'style':
                self.style = kwargs['style']
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
