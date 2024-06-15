import json


def RenderCSS(style):
    if isinstance(style, str):
        return style
    css = ''
    for prop in style:
        if prop.startswith('@'):
            if prop == '@imports':
                for i in style[prop]:
                    css += f"@import url('{i}'); "
            else:
                f = ''
                while True:
                    try:
                        for inprop in style[prop]:
                            if inprop.startswith('@'):
                                f = f'({inprop.removeprefix("@")}: {style[prop][inprop]})'
                                style[prop].pop(inprop)
                        break
                    except:
                        pass
                css += f'{prop} {f} '
                css += ('{ ' + RenderCSS(style[prop]) + '}')
        elif isinstance(style[prop], list):
            css += f'{prop}:{", ".join(style[prop])};'
        elif isinstance(style[prop], str):
            css += f'{prop}:{style[prop]};'
        elif isinstance(style[prop], int):
            css += f'{prop}:{style[prop]};'
        elif isinstance(style[prop], list):
            css += f'{prop}:{", ".join(style[prop])};'
        else:
            css += f'{prop} '
            css += ('{ ' + RenderCSS(style[prop]) + '}')
        css += ' '
    return css


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


Title = lambda innertext, **kwargs: Widget('h1', innertext=innertext, **kwargs)
Box = lambda **kwargs: Widget('div', selector='the_box', **kwargs)
Line = lambda childs, **kwargs: Widget('p', childs=childs if isinstance(childs, list) else [childs], **kwargs)
Label = lambda innertext, **kwargs: Line(childs=innertext, **kwargs)
Textbox = lambda name, selector = '', **kwargs: Widget('input', name=name, id=name, selector=f'textbox {selector}', **kwargs)
Button = lambda selector = '', **kwargs: Widget('button', selector=f'button {selector}', **kwargs)
Form = lambda method, childs: Widget('form', method=method, childs=childs)
Bold = lambda innertext: Widget('b', innertext=innertext)
Italic = lambda innertext: Widget('i', innertext=innertext)
Link = lambda innertext, url, external=False: Widget('a', innertext=innertext, href=url, selector='link', **({'target': '_blank'} if external else {}))


class Page:
    def __init__(self, **kwargs):
        self.content = []
        self.data = {
            'lang': 'en',
            'charset': 'UTF-8',
            'viewport': {
                'width': 'device-width',
                'initial-scale': '1.0'
            },
            'description': 'BevyFrame App',
            'keywords': [],
            'author': '',
            'icon': {
                'href': '/Static/favicon.ico',
                'type': 'image/x-icon'
            },
            'title': 'WebApp',
            'OpenGraph': {
                'title': 'WebApp',
                'description': 'BevyFrame App',
                'image': '/Static/Banner.png',
                'url': '',
                'type': 'website'
            },
            'selector': ''
        }
        self.db = {}
        self.style = {}
        for arg in kwargs:
            if arg == 'childs':
                self.content = kwargs['childs']
            elif arg == 'style':
                self.style = kwargs['style']
            else:
                self.data.update({arg: kwargs[arg]})

    def __getattr__(self, item):
        return self.data[item]

    def __repr__(self):
        return self.render()

    def render(self):
        og = []
        for i in self.OpenGraph:
            og.append(Widget('meta', name=f'og:{i}', content=self.OpenGraph[i]))
        html = '<!DOCTYPE html>'
        html += Widget('html', lang=self.lang, childs=[
            Widget('head', childs=[
                                      Widget('meta', charset=self.charset),
                                      Widget('meta', name='viewport',
                                             content=f'width={self.viewport["width"]}, initial-scale={self.viewport["initial-scale"]}'),
                                      Widget('meta', name='description', content=self.description),
                                      Widget('meta', name='keywords', content=', '.join(self.keywords)),
                                      Widget('meta', name='author', content=self.author),
                                      Widget('link', rel='icon', href=self.icon['href'], type=self.icon['type']),
                                      Widget('title', innertext=self.title)
                                  ] + og + [
                                      Widget('script', innertext=f'const bf_db = {json.dumps(self.db)}'),
                                      Widget('style', innertext=RenderCSS(self.style))
                                  ]),
            Widget('body', selector=self.selector, childs=self.content)
        ]).render()
        return html
