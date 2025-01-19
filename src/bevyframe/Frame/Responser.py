import importlib.util
import json
import os
import subprocess
import traceback
import importlib.metadata
from datetime import datetime, UTC
from bevyframe.Features.Login import get_session_token
from bevyframe.Features.ServiceWorker import service_worker
from bevyframe.Features.WebManifest import web_manifest
from bevyframe.Helpers.Exceptions import Error404
from bevyframe.Helpers.MatchRouting import match_routing
from bevyframe.Objects.Activity import Activity
from bevyframe.Objects.Context import Context
from bevyframe.Features.Style import compile_object as compile_to_css
from bevyframe.Features.Bridge import process_proxy
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page
from bevyframe.Widgets.Widget import Widget
import mimetypes



def responser(self, recv: dict[str, (str, dict)], req_time: str, r: Context, display_status_code: bool) -> tuple[any, bool]:
    resp = None
    path = recv['path']
    reverse_routes = self.reverse_routes
    if path == '/.well-known/bevyframe/proxy':
        resp = r.create_response(process_proxy(r))
    elif 'PWA' not in self.disabled and path == '/.well-known/bevyframe/pwa.webmanifest':
        resp = r.create_response(web_manifest())
    elif 'PWA' not in self.disabled and path == '/sw.js':
        resp = r.create_response(service_worker())
        resp.headers['Content-Type'] = 'application/javascript'
    elif path.startswith('/assets/'):
        file_path = f"./{path}"
        while '//' in file_path:
            file_path = file_path.replace('//', '/')
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                resp = r.create_response(
                    f.read(),
                    headers={
                        'Content-Type': mimetypes.types_map.get(f".{file_path.split('.')[-1]}", 'plain/text'),
                        'Content-Length': len(f.read()),
                        'Connection': 'keep-alive'
                    }
                )
    elif recv['method'].lower() == 'options':
        resp = r.create_response(status_code=204)
    if "DynamicRouting" not in self.disabled and path in reverse_routes:
        path = reverse_routes[path]
        while '<' in path:
            p1 = path.split('<')[0]
            var = path.removeprefix(p1 + '<').split('>')[0]
            p2 = path.removeprefix(p1 + '<' + var + '>')
            path = p1 + r.query.get(var) + p2
        resp = r.start_redirect(path)
    elif "DynamicRouting" not in self.disabled and path in self.routes:
        resp = self.routes[path](r)
        if resp is None:
            in_routes = False
            for rt in self.routes:
                if not in_routes:
                    match, variables = match_routing(rt, path)
                    in_routes = match
                    for v in variables:
                        r.query.update({v: variables[v]})
                    if in_routes:
                        if callable(self.routes[rt]):
                            resp = self.routes[rt](r)
                        else:
                            path = self.routes[rt]
    # noinspection PyBroadException
    try:
        if resp is None:
            file_path = f"./pages/{path}"
            for i in range(0, 2):
                file_path = file_path.replace('//', '/')
            if not os.path.isfile(file_path):
                file_path += '/__init__.py'
            if not os.path.isfile(file_path):
                raise Error404
            if file_path.endswith('.py'):
                page_script_spec = importlib.util.spec_from_file_location(
                    os.path.splitext(os.path.basename(file_path))[0],
                    file_path
                )
                page_script = importlib.util.module_from_spec(page_script_spec)
                page_script_spec.loader.exec_module(page_script)
                if 'AccessControl' not in self.disabled:
                    if 'whitelist' in page_script.__dict__:
                        if r.email not in page_script.whitelist():
                            return self.error_handler(r, 401, ''), True
                    elif 'blacklist' in page_script.__dict__:
                        if r.email in page_script.blacklist():
                            return self.error_handler(r, 401, ''), True
                if 'CustomLogging' not in self.disabled:
                    if 'log' in page_script.__dict__:
                        formatted_log = page_script.log(r, req_time)
                        if formatted_log is not None:
                            if isinstance(formatted_log, tuple):
                                display_status_code = formatted_log[1]
                                formatted_log = formatted_log[0]
                            print('\r' + ''.join([' ' for _ in range(len(recv['log']))]), end='', flush=True)
                            print(f'\r(   ) ', end='', flush=True)
                            print(formatted_log.replace('\n', '').replace('\r', ''), end='', flush=True)
                if recv['headers'].get('Accept', '') == 'application/activity+json':
                    if 'activity' in page_script.__dict__:
                        resp = page_script.activity(r)
                        if isinstance(resp, Activity):
                            resp = resp.render()
                        else:
                            resp = self.error_handler(r, 500, 'Activity must return `Activity`')
                    else:
                        raise AttributeError(f"'{r.path}' has no attribute 'activity'")
                elif recv['method'].lower() in page_script.__dict__:
                    resp = getattr(page_script, recv['method'].lower())(r)
                elif 'application' in page_script.__dict__:
                    return getattr(page_script, 'application'), display_status_code
                else:
                    resp = self.error_handler(r, 405, '')
            elif file_path.endswith('.html'):
                resp = r.render_template(file_path.removeprefix('./pages/'))
            elif "x" in subprocess.check_output(["ls", "-l", file_path]).decode().strip().strip('\n').split(' ')[0]:
                with open('.request', 'w') as f:
                    f.write(str(r))
                with open('.body', 'wb') as f:
                    f.write(r.body.encode() if isinstance(r.body, str) else r.body)
                lines: list[bytes] = bytes(subprocess.check_output([file_path])).split(b'\n')
                os.remove('.request')
                os.remove('.body')
                _p, status_code, *_a = lines.pop(0).split(b' ')
                status_code = int(status_code.decode())
                headers = {}
                while lines[0] != b'':
                    l = lines.pop(0)
                    t = l.split(b': ', 1)
                    headers.update({t[0].decode(): t[1].decode()})
                lines.pop(0)
                body = b'\n'.join(lines)
                resp = r.create_response(body, headers=headers, status_code=status_code)
    except Error404:
        pass
    except Exception:
        resp = self.error_handler(r, 500, traceback.format_exc())
    if resp is None:
        resp = self.error_handler(r, 404, '')
    if isinstance(resp, Page):
        if 'Widgets' in self.disabled:
            resp = 'Widgets are disabled'
        else:
            resp.data['icon'] = {
                'href': self.icon,
                'type': mimetypes.types_map[f".{self.icon.split('.')[-1]}"]
            } if resp.data['icon'] == {
                'href': '/favicon.ico',
                'type': 'image/x-icon'
            } else resp.data['icon']
            resp.style = self.style + compile_to_css(resp.style)
            if recv['path'] == '/':
                resp.content.append(Widget('script', innertext="if (typeof navigator.serviceWorker !== 'undefined') navigator.serviceWorker.register('sw.js');"))
    elif 'Templating' not in self.disabled and isinstance(resp, str) and resp.startswith('<!DOCTYPE html>'):
        if recv['path'] == '/':
            resp += "<script>if (typeof navigator.serviceWorker !== 'undefined') navigator.serviceWorker.register('sw.js');</script>"
    if not isinstance(resp, Response):
        resp = r.create_response(resp)
    if isinstance(resp.body, dict) or isinstance(resp.body, list):
        resp.body = json.dumps(resp.body)
    elif isinstance(resp.body, Page):
        resp.body = resp.body.render().encode()
    # noinspection PyTypeChecker
    resp.headers['Content-Length'] = len(resp.body.encode() if isinstance(resp.body, str) else resp.body)
    resp.headers['Server'] = f"BevyFrame/{importlib.metadata.version('bevyframe')}"
    resp.headers['Access-Control-Allow-Origin'] = '*' if self.cors else f"https://{recv['headers'].get('Host', '')}"
    resp.headers['Access-Control-Max-Age'] = '86400'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, CONNECT, TRACE'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-PINGOTHER, Authorization'
    resp.headers['Access-Control-Allow-Credentials'] = 'Content-Type, X-PINGOTHER, Authorization'
    resp.headers['Strict-Transport-Security'] = 'max-age=86400'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = resp.headers['X-Frame-Options'] if 'X-Frame-Options' in resp.headers else 'DENY'
    resp.headers['X-XSS-Protection'] = '1; mode = block'
    resp.headers['Cache-Control'] = 'private'
    resp.headers['Accept-CH'] = 'Device-Memory, Downlink, ECT'
    resp.headers['Expires'] = '0'
    resp.headers['Date'] = datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')
    if resp.credentials['email'] != r.email:
        resp.headers['Set-Cookie'] = 's=' + get_session_token(self.secret, **resp.credentials) + ';'
    else:
        resp.headers['Set-Cookie'] = recv['headers'].get('Cookie', '')
    if 'TheProtocols' not in self.disabled:
        if r and hasattr(r.data, 'is_edited') and r.data.is_edited():
            r.user.data(dict(r.data))
        if r and hasattr(r.preferences, 'is_edited') and r.preferences.is_edited():
            r.user.preferences(dict(r.preferences))
    return resp, display_status_code
