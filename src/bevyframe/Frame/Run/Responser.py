import importlib.util
import json
import os
import traceback

from TheProtocols.Data import DataRoot

from bevyframe.Features.Login import get_session_token
from bevyframe.Helpers.Identifiers import mime_types
from bevyframe.Helpers.MatchRouting import match_routing
from bevyframe.Objects.Request import Request
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page


def responser(self, recv, req_time, r, default_network):
    resp = None
    # noinspection PyBroadException
    try:
        in_routes = False
        if recv['path'] in self.routes:
            in_routes = True
            resp = self.routes[recv['path']](r)
        else:
            for rt in self.routes:
                if not in_routes:
                    match, variables = match_routing(rt, recv['path'])
                    in_routes = match
                    if in_routes:
                        resp = self.routes[rt](r, **variables)
            if resp is None:
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
                            if 'whitelist' in page_script.__dict__:
                                if r.email not in page_script.whitelist():
                                    return self.error_handler(r, 401, '')
                            elif 'blacklist' in page_script.__dict__:
                                if r.email in page_script.blacklist():
                                    return self.error_handler(r, 401, '')
                            if recv['method'].lower() in page_script.__dict__:
                                if 'log' in page_script.__dict__:
                                    formatted_log = page_script.log(r, req_time)
                                    if formatted_log is not None:
                                        print(f'\r(   ) ', end='', flush=True)
                                        print(
                                            '                   ' if r.email.split('@')[0] == 'Guest' else
                                            ''.join([' ' for i in range(len(r.email))])
                                        , end='', flush=True)
                                        print('                       ', end='', flush=True)
                                        print(''.join([' ' for i in range(len(r.method))]), end='', flush=True)
                                        print(''.join([' ' for i in range(len(r.path))]), end='', flush=True)
                                        print('        ', end='', flush=True)
                                        print(f'\r(   ) ', end='', flush=True)
                                        print(
                                            formatted_log.replace('\n', '').replace('\r', '')
                                            , end='', flush=True)
                                resp = getattr(page_script, recv['method'].lower())(r)
                            else:
                                resp = self.error_handler(r, 405, '')
                        except FileNotFoundError:
                            resp = self.error_handler(r, 404, '')
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
                    resp = self.error_handler(r, 404, '')
    except Exception:
        resp = self.error_handler(r, 500, traceback.format_exc())
    if resp is None:
        resp = self.error_handler(r, 404, '')
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
    try:
        resp.headers['Set-Cookie'] = 's=' + get_session_token(self.secret, **(
            resp.credentials if resp.credentials != {} else recv['credentials']
        )) + '; '
    except TypeError:
        resp.headers['Set-Cookie'] = 's=' + get_session_token(self.secret, email=f'Guest@{default_network}', password='') + '; '
    DataRoot(r.user, self.package)(r.data)
    return resp
