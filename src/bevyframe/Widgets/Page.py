import json


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
            if arg == 'children':
                self.content = kwargs['children']
            elif arg == 'style':
                self.style = kwargs['style']
            elif arg == 'db':
                self.db = kwargs['db']
            elif arg == 'color':
                self.data.update({'selector': f"body_{kwargs['color']}"})
                self.color = kwargs['color']
            else:
                self.data.update({arg: kwargs[arg]})

    def __getattr__(self, item) -> any:
        return self.data[item]

    def __repr__(self) -> str:
        return self.bf_widget()

    def stdout(self) -> str:
        p1 = '\n'.join([
            f"Response.{k}: {v}"
            for k, v in {
                "Type": "Page",
                "Charset": self.charset,
                "Viewport": f'width={self.viewport["width"]}, initial-scale={self.viewport["initial-scale"]}, maximum-scale=1, user-scalable=0',
                "Description": self.description,
                "Author": self.author,
                "Icon": self.icon['href'],
                "Title": self.title,
                "Data": self.db,
                "ThemeColor": self.color,
            }.items()
        ])
        p2 = '\n'.join([
            f"Response.OpenGraph.{k}: {v}"
            for k, v in self.OpenGraph.items()
        ])
        p3 = json.dumps([
            i.bf_widget() if hasattr(i, 'bf_widget') else str(i)
            for i in self.content
        ])
        return p1 + '\n' + p2 + '\n\n' + p3
