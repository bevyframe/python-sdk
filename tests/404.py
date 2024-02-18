from bevyframe import Page, Widget
import json


def get(request) -> Page:
    return Page(
        lang='',
        charset='UTF-8',
        viewport={
            'width': 'device-width',
            'initial-scale': '1.0'
        },
        description='BevyFrame Test App',
        keywords=['Test'],
        author='islekcaganmert@barsposta.com',
        icon={
            'href': '/Static/favicon.ico',
            'type': 'image/x-icon'
        },
        title='BevyFrame Test App',
        OpenGraph={
            'title': 'WebApp',
            'description': 'BevyFrame App',
            'image': '/Static/Banner.png',
            'url': '',
            'type': 'website'
        },
        style=json.loads(open('index.css.json', 'rb').read()),
        selector='body_blue',
        childs=[
            Widget('h1', innertext=f'404 Not Found')
        ]
    )