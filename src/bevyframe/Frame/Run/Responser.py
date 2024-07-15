import importlib.util
import json
import os
import traceback

from bevyframe.Features.Login import get_session_token
from bevyframe.Helpers.Identifiers import mime_types
from bevyframe.Helpers.MatchRouting import match_routing
from bevyframe.Objects.Request import Request
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page


def responser(self, recv):
    resp = None
    # noinspection PyBroadException
    try:
        in_routes = False
        if recv['path'] in self.routes:
            in_routes = True
            resp = self.routes[recv['path']]()
        for rt in self.routes:
            if not in_routes:
                match, variables = match_routing(rt, recv['path'])
                in_routes = match
                if in_routes:
                    resp = self.routes[rt](Request(recv, self), **variables)
                else:
                    page_script_path = f"./{recv['path']}"
                    for i in range(0, 3):
                        page_script_path = page_script_path.replace('//', '/')
                    if not os.path.isfile(page_script_path):
                        page_script_path += '/__init__.py'
                    if os.path.isfile(page_script_path):
                        if page_script_path.endswith('.py'):
                            page_script_spec = importlib.util.spec_from_file_location(
                                os.path.splitext(os.path.basename(page_script_path))[0],
                                page_script_path
                            )
                            page_script = importlib.util.module_from_spec(page_script_spec)
                            try:
                                page_script_spec.loader.exec_module(page_script)
                                if recv['method'].lower() in page_script.__dict__:
                                    resp = getattr(page_script, recv['method'].lower())(Request(recv, self))
                                else:
                                    resp = self.error_handler(Request(recv, self), 405, '')
                            except FileNotFoundError:
                                resp = self.error_handler(Request(recv, self), 404, '')
                        else:
                            with open(page_script_path, 'rb') as f:
                                resp = Response(
                                    (f.read().decode() if page_script_path.endswith('.html') else f.read()),
                                    headers={
                                        'Content-Type': mime_types.get(
                                            page_script_path.split('.')[-1],
                                            'application/octet-stream'
                                        ),
                                        'Content-Length': len(f.read()),
                                        'Connection': 'keep-alive'
                                    }
                                )
                    else:
                        resp = self.error_handler(Request(recv, self), 404, '')
    except Exception:
        resp = self.error_handler(Request(recv, self), 500, traceback.format_exc())
    if resp is None:
        resp = self.error_handler(Request(recv, self), 404, '')
    if isinstance(resp, Page):
        resp.data['lang'] = ''
        resp.data['charset'] = 'utf-8'
        resp.data['viewport'] = {
            'width': 'device-width',
            'initial-scale': '1.0'
        }
        resp.data['keywords'] = self.keywords
        resp.data['author'] = self.developer
        resp.data['icon'] = {
            'href': self.icon,
            'type': mime_types[self.icon.split('.')[-1]]
        }
        if 'OpenGraph' not in resp.data:
            resp.data['OpenGraph'] = {
                'title': 'WebApp',
                'description': 'BevyFrame App',
                'image': '/Static/Banner.png',
                'url': '',
                'type': 'website'
            }
        resp.style = self.style
    if not isinstance(resp, Response):
        resp = Response(resp)
    if isinstance(resp.body, Page):
        resp.body = resp.body.render()
    elif isinstance(resp.body, dict):
        resp.body = json.dumps(resp.body)
    elif isinstance(resp.body, list):
        resp.body = json.dumps(resp.body)
    resp.headers['Content-Length'] = len(resp.body.encode() if isinstance(resp.body, str) else resp.body)
    resp.headers['Set-Cookie'] = 's=' + get_session_token(self.secret, **(
        resp.credentials if resp.credentials != {} else recv['credentials']
    )) + '; '
    return resp
