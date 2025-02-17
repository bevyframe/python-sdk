import importlib.resources
import json
import bevyframe.Features.Style as Style
from bevyframe.Features.BridgeJS import client_side_bridge


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
        return self.bf_widget()

    def render(self) -> str:
        og = []
        for i in self.OpenGraph:
            og.append(f'<meta name="og:{i}" content="{self.OpenGraph[i]}">')
        body = [i.bf_widget() if hasattr(i, 'bf_widget') else str(i) for i in self.content]
        html = f"""
            <!DOCTYPE html>
            <html lang="{self.data['lang']}">
                <head>
                    <meta charset="{self.charset}" />
                    <meta name="viewport" content="width={self.viewport["width"]}, initial-scale={self.viewport["initial-scale"]}, maximum-scale=1, user-scalable=0" />
                    <meta name="description" content="{self.description}" />
                    <meta name="author" content="{self.author}" />
                    <link rel="manifest" href="/.well-known/bevyframe/pwa.webmanifest" />
                    <link rel="icon" href="{self.icon["href"]}" type="{self.icon["type"]}" />
                    <title>{self.title}</title>
                    {''.join(og)}
                    <script>
                        const bf_db = {json.dumps(self.db)};
                        { importlib.resources.files('bevyframe').joinpath('Scripts/renderWidget.js').read_text().replace('`---body---`', json.dumps(body)) }
                        if (typeof navigator.serviceWorker !== 'undefined') navigator.serviceWorker.register('sw.js');
                        {client_side_bridge()}
                    </script>
                    <style>{Style.compile_object(self.style)}</style>
                </head>
                <body class="{self.selector}" onload="renderAll()"></body>
            </html>
        """
        while '  ' in html:
            html = html.replace('  ', ' ')
        return html
