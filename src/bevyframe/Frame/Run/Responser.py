import importlib.util
import json
import os
import traceback
import importlib.metadata
from datetime import datetime, UTC
import jinja2
from bevyframe.Features.Login import get_session_token
from bevyframe.Helpers.Exceptions import Error404
from bevyframe.Helpers.Identifiers import mime_types
from bevyframe.Helpers.MatchRouting import match_routing
from bevyframe.Objects.Context import Context
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page
from bevyframe.Features.Style import compile_object as compile_to_css
from bevyframe.Features.Bridge import process_proxy


def responser(self, recv, req_time, r: Context, display_status_code: int):
    resp = None
    path = recv['path']
    reverse_routes = self.reverse_routes
    if path == '/.well_known/bevyframe/proxy':
        resp = process_proxy(r)
    elif path.startswith('/assets/'):
        file_path = f"./{path.split('?')[0]}"
        for _ in range(0, 3):
            file_path = file_path.replace('//', '/')
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                resp = r.create_response(
                    f.read(),
                    headers={
                        'Content-Type': mime_types.get(
                            file_path.split('.')[-1],
                            'plain/text'
                        ),
                        'Content-Length': len(f.read()),
                        'Connection': 'keep-alive'
                    }
                )
    elif recv['method'].lower() == 'options':
        resp = r.create_response(status_code=204)
    elif path.split('?')[0] in reverse_routes:
        path = reverse_routes[path.split('?')[0]]
        while '<' in path:
            p1 = path.split('<')[0]
            var = path.removeprefix(p1 + '<').split('>')[0]
            p2 = path.removeprefix(p1 + '<' + var + '>')
            path = p1 + r.query.get(var) + p2
        resp = r.start_redirect(path)
    else:
        # noinspection PyBroadException
        try:
            in_routes = False
            if path.split('?')[0] in self.routes:
                resp = self.routes[path.split('?')[0]](r)
            else:
                for rt in self.routes:
                    if not in_routes:
                        match, variables = match_routing(rt, path.split('?')[0])
                        in_routes = match
                        for v in variables:
                            r.query.update({v: variables[v]})
                        if in_routes:
                            if callable(self.routes[rt]):
                                resp = self.routes[rt](r)
                            else:
                                path = self.routes[rt]
                if resp is None:
                    file_path = f"./pages/{path.split('?')[0]}"
                    for i in range(0, 3):
                        file_path = file_path.replace('//', '/')
                    if not os.path.isfile(file_path):
                        file_path += '/__init__.py'
                    if os.path.isfile(file_path):
                        if file_path.endswith('.py'):
                            page_script_spec = importlib.util.spec_from_file_location(
                                os.path.splitext(os.path.basename(file_path))[0],
                                file_path
                            )
                            page_script = importlib.util.module_from_spec(page_script_spec)
                            try:
                                page_script_spec.loader.exec_module(page_script)
                                if 'whitelist' in page_script.__dict__:
                                    if r.email not in page_script.whitelist():
                                        return self.error_handler(r, 401, ''), True
                                elif 'blacklist' in page_script.__dict__:
                                    if r.email in page_script.blacklist():
                                        return self.error_handler(r, 401, ''), True
                                if recv['method'].lower() in page_script.__dict__:
                                    if 'log' in page_script.__dict__:
                                        formatted_log = page_script.log(r, req_time)
                                        if formatted_log is not None:
                                            if isinstance(formatted_log, tuple):
                                                display_status_code = formatted_log[1]
                                                formatted_log = formatted_log[0]
                                            print('\r' + ''.join([' ' for _ in range(len(recv['log']))]), end='', flush=True)
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
                            if file_path.endswith('.html'):
                                resp = r.render_template(file_path.removeprefix('./pages/'))
                            else:
                                with open(file_path, 'rb') as f:
                                    resp = r.create_response(
                                        f.read(),
                                        headers={
                                            'Content-Type': mime_types.get(
                                                file_path.split('.')[-1],
                                                'plain/text'
                                            ),
                                            'Content-Length': len(f.read()),
                                            'Connection': 'keep-alive'
                                        }
                                    )
        except Error404:
            resp = self.error_handler(r, 404, '')
        except Exception:
            resp = self.error_handler(r, 500, traceback.format_exc())
    if resp is None:
        resp = self.error_handler(r, 404, '')
    if isinstance(resp, Page):
        resp.data['icon'] = {
            'href': self.icon,
            'type': mime_types[self.icon.split('.')[-1]]
        } if resp.data['icon'] == {
            'href': '/favicon.ico',
            'type': 'image/x-icon'
        } else resp.data['icon']
        resp.style = self.style + compile_to_css(resp.style)
    if not isinstance(resp, Response):
        resp = r.create_response(resp)
    if isinstance(resp.body, Page):
        resp.body = resp.body.render()
    elif isinstance(resp.body, dict):
        resp.body = json.dumps(resp.body)
    elif isinstance(resp.body, list):
        resp.body = json.dumps(resp.body)
    resp.headers['Content-Length'] = len(resp.body.encode() if isinstance(resp.body, str) else resp.body)
    resp.headers['Server'] = f"BevyFrame/{importlib.metadata.version('bevyframe')}"
    resp.headers['Access-Control-Allow-Origin'] = '*' if self.cors else f"https://{recv['headers'].get('Host', '')}"
    resp.headers['Access-Control-Max-Age'] = '86400'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, CONNECT, TRACE'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-PINGOTHER, Authorization'
    resp.headers['Vary'] = 'Origin, Accept-Encoding'
    resp.headers['Date'] = datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')
    try:
        if resp.credentials['email'] != r.email:
            resp.headers['Set-Cookie'] = 's=' + get_session_token(self.secret, **resp.credentials) + ';'
            print('\n', resp.credentials['email'], '\n', r.email, '\n', resp.headers['Set-Cookie'])
        else:
            resp.headers['Set-Cookie'] = recv['headers'].get('Cookie', '')
    except TypeError:
        resp.headers['Set-Cookie'] = recv['headers'].get('Cookie', '')
    if r and hasattr(r.data, 'is_edited') and r.data.is_edited():
        r.user.data(dict(r.data))
    if r and hasattr(r.preferences, 'is_edited') and r.preferences.is_edited():
        r.user.preferences(dict(r.preferences))
    return resp, display_status_code
