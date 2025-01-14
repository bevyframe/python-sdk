import json
import bevyframe.Features.Style as Style
from bevyframe.Features.BridgeJS import client_side_bridge
from bevyframe.Widgets.Widget import Widget


class Page:
    def __init__(self, **kwargs) -> None:
        self.content = []
        self.data = {
            'lang': 'en',
            'charset': 'UTF-8',
            'viewport': {
                'width': 'device-width',
                'initial-scale': '1.0'
            },
            'description': 'BevyFrame App',
            'author': '',
            'icon': {
                'href': '/favicon.ico',
                'type': 'image/x-icon'
            },
            'title': 'WebApp',
            'OpenGraph': {
                'title': 'WebApp',
                'description': 'BevyFrame App',
                'image': '/Banner.png',
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
            elif arg == 'db':
                self.db = kwargs['db']
            elif arg == 'color':
                self.data.update({'selector': f"body_{kwargs['color']}"})
            else:
                self.data.update({arg: kwargs[arg]})

    def __getattr__(self, item) -> any:
        return self.data[item]

    def __repr__(self) -> str:
        return self.render()

    def render(self) -> str:
        og = []
        for i in self.OpenGraph:
            og.append(Widget('meta', name=f'og:{i}', content=self.OpenGraph[i]))
        html = '<!DOCTYPE html>'
        html += Widget('html', lang=self.lang, childs=[
            Widget(
                'head',
                childs=[
                    Widget('meta', charset=self.charset),
                    Widget('meta', name='viewport', content=f'width={self.viewport["width"]}, initial-scale={self.viewport["initial-scale"]}'),
                    Widget('meta', name='description', content=self.description),
                    Widget('meta', name='author', content=self.author),
                    Widget('link', rel='manifest', href='/.well-known/bevyframe/pwa.webmanifest'),
                    Widget('link', rel='icon', href=self.icon['href'], type=self.icon['type']),
                    Widget('title', innertext=self.title)
                ] + og + [
                    Widget('script', innertext=f'const bf_db = {json.dumps(self.db)}'),
                    Widget('script', innertext=client_side_bridge()),
                    Widget('style', innertext=Style.compile_object(self.style))
                ]
            ),
            Widget('body', selector=self.selector, childs=self.content)
        ]).render()
        return html
