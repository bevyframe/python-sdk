import importlib.util
import json
import os
import traceback
import importlib.metadata
from datetime import datetime, UTC
import jinja2
from bevyframe.Features.Login import get_session_token, get_session
from bevyframe.Helpers.Exceptions import Error404
from bevyframe.Helpers.Identifiers import mime_types
from bevyframe.Helpers.MatchRouting import match_routing
from bevyframe.Objects.Context import Context
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page
from bevyframe.Features.Style import compile_object as compile_to_css


def responser(self, recv, req_time, r: Context, display_status_code: int):
    resp = None
    if recv['method'].lower() == 'options':
        resp = r.create_response(status_code=204)
    else:
        # noinspection PyBroadException
        try:
            in_routes = False
            if recv['path'].split('?')[0] in self.routes:
                resp = self.routes[recv['path'].split('?')[0]](r)
            else:
                for rt in self.routes:
                    if not in_routes:
                        match, variables = match_routing(rt, recv['path'].split('?')[0])
                        in_routes = match
                        if in_routes:
                            resp = self.routes[rt](r, **variables)
                if resp is None:
                    page_script_path = f"./{recv['path'].split('?')[0]}"
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
                                            print('\r' + ''.join([' ' for i in range(len(recv['log']))]), end='', flush=True)
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
                                if page_script_path.endswith('.html'):
                                    body = jinja2.Template(f.read().decode()).render(request=r, style=f"<style>{self.style}</style>")
                                    resp = r.create_response(
                                        body,
                                        headers={
                                            'Content-Type': 'text/html',
                                            'Content-Length': len(body),
                                            'Connection': 'keep-alive'
                                        }
                                    )
                                else:
                                    resp = r.create_response(
                                        f.read(),
                                        headers={
                                            'Content-Type': mime_types.get(
                                                page_script_path.split('.')[-1],
                                                'application/octet-stream'
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
        resp.data['keywords'] = self.keywords if resp.data['keywords'] == [] else resp.data['keywords']
        resp.data['author'] = self.developer if resp.data['author'] == '' else resp.data['author']
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
    resp.headers['Connection'] = 'Keep-Alive'
    resp.headers['Date'] = datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')
    try:
        if resp.credentials['email'] != r.email:
            resp.headers['Set-Cookie'] = 's=' + get_session_token(self.secret, **resp.credentials) + ';'
        else:
            resp.headers['Set-Cookie'] = recv['headers'].get('Cookie', '')
    except TypeError:
        resp.headers['Set-Cookie'] = recv['headers'].get('Cookie', '')
    if r and hasattr(r.data, 'is_edited') and r.data.is_edited():
        r.user.data(dict(r.data))
    if r and hasattr(r.preferences, 'is_edited') and r.preferences.is_edited():
        r.user.preferences(dict(r.preferences))
    return resp, display_status_code
