import urllib.parse
from datetime import datetime
from typing import Any
import importlib.util
import importlib
import traceback
import getpass
import socket
import os
import re
from .widgets import *
from .login import *
import requests
import TheProtocols


https_codes = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    405: 'Method Not Allowed',
    404: 'Not Found',
    410: 'Gone',
    415: 'Unsupported Media Type',
    418: 'I\'m a teapot',
    429: 'Too Many Requests',
    451: 'Unavailable For Legal Reasons',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    506: 'Variant Also Negotiates',
    511: 'Network Authentication Required'
}
admins = {}
mime_types = {
    'html': 'text/html',
    'txt': 'text/plain',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'pdf': 'application/pdf',
    'ico': 'image/x-icon',
    'css': 'text/css',
    'json': 'application/json'
}


def match_routing(param_str: str, path: str) -> (bool, dict):
    regex_str = param_str.replace('*', '.*')
    variables = re.findall(r'<(.*?)>', regex_str)
    for var in variables:
        regex_str = regex_str.replace(f'<{var}>', f'(?P<{var}>.*?)')
    regex_str = regex_str.replace('/', '\\/')
    regex = re.compile(f'^{regex_str}$')
    match = regex.match(path)
    if match:
        variable_values = {key: value for key, value in match.groupdict().items() if value}
        return True, variable_values
    else:
        return False, {}


class Request:
    def __init__(self, data: dict[str], app) -> None:
        self.method = data['method']
        self.path = data['path']
        self.headers = data['headers']
        self.body = urllib.parse.unquote(data['body'])
        self.form = {}
        for b in self.body.split('\r\n'):
            for i in b.split('&'):
                if '=' in i:
                    self.form.update({i.split('=')[0]: i.split('=')[1]})
        try:
            self.email = data['credentials']['email']
            self.password = data['credentials']['password']
            self.user = TheProtocols.ID(self.email, self.password)
        except TypeError:
            pass
        self.app = app
        self.cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split('; '):
                if '=' in cookie:
                    self.cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})

    def __getattr__(self, item) -> Any:
        if item == 'json':
            return json.loads(self.body)


class Response:
    def __init__(self, body: (Page, str, dict, list), **kwargs) -> None:
        self.body = body
        self.credentials = {}
        self.headers = {'Content-Type': 'text/html; charset=utf-8'}
        self.status_code = 200
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def login(self, email, password) -> None:
        self.credentials = {'email': email, 'password': password}


def redirect(url) -> Response:
    return Response('', headers={'Location': url}, status_code=303)


def get_admin(package) -> dict:
    return admins[package]


class Frame:
    def __init__(self, package, developer, administrator, secret, style, icon='/favicon.ico', keywords=None) -> None:
        if keywords is None:
            keywords = []
        self.secret = secret
        self.package = package
        self.debug = False
        self.developer = developer
        self.routes = {}
        if isinstance(style, dict):
            self.style = style
        elif isinstance(style, str):
            if os.path.isfile(style):
                self.style = json.load(open(style, 'rb'))
            elif style.startswith('https://'):
                r = requests.get(style)
                if r.status_code == 200:
                    self.style = r.json()
                else:
                    self.style = {}
            else:
                self.style = {}
        else:
            self.style = {}
        self.icon = icon
        self.keywords = keywords
        if administrator:
            self.admin = TheProtocols.ID(administrator, getpass.getpass(f'Password for {administrator}: '))
            print()
            print(f"Welcome {self.admin.id}!")
        print()

    def route(self, path, whitelist: list = None, blacklist: list = None) -> Any:
        def decorator(func) -> Any:
            self.routes.update({path: func})

            def wrapper(r: Request, **kwargs) -> Any:
                return func(r, **kwargs)
            return wrapper
        return decorator

    def error_handler(self, request, status_code, exception) -> Response:
        # noinspection PyBroadException
        try:
            page_script_spec = importlib.util.spec_from_file_location(
                os.path.splitext(os.path.basename(f"./{status_code}.py"))[0],
                f"./{status_code}.py"
            )
            page_script = importlib.util.module_from_spec(page_script_spec)
            page_script_spec.loader.exec_module(page_script)
            return getattr(page_script, 'get')(request)
        except:
            t = exception.replace('\n', '<br>').split('<br>  File')
            e_boxes = [
                Widget(
                    'h1',
                    innertext=f'{https_codes[status_code]}'
                )
            ]
            if self.debug:
                for e in t:
                    if e.startswith('Traceback'):
                        e_boxes.append(
                            Widget(
                                'div',
                                style={'margin-bottom': '10px', 'padding-top': '10px', 'font-family': 'monospace'},
                                innertext=e
                            )
                        )
                    elif 'site-packages' in e:
                        e_boxes.append(
                            Widget(
                                'div',
                                selector='the_box',
                                style={'margin-bottom': '10px', 'padding-top': '10px', 'font-family': 'monospace'},
                                innertext=(
                                    'Module ' +
                                    e.split('site-packages/')[1].split('/')[0] + ', ' +
                                    'file ' +
                                    e.split('site-packages/' + e.split('site-packages/')[1].split('/')[0] + '/')[1].split('"')[0] +
                                    e.removeprefix(e.split(',')[0])
                                )
                            )
                        )
                    else:
                        e_boxes.append(
                            Widget(
                                'div',
                                selector='the_box',
                                style={'margin-bottom': '10px', 'padding-top': '10px', 'font-family': 'monospace'},
                                innertext=(
                                    'Path ' +
                                    e.split('"')[1].removeprefix('.').removesuffix('/__init__.py').removeprefix(os.getcwd()) +
                                    e.removeprefix(e.split('"')[0] + '"' + e.split('"')[1] + '"')
                                )
                            )
                        )
            return Response(
                body=Page(
                    title=https_codes[status_code],
                    style=self.style,
                    childs=e_boxes,
                    selector=f'body_{request.user.id.settings.theme_color}'
                ),
                status_code=status_code
            )

    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
        print('BevyFrame 0.2 ⍺')
        print('Upstream Version, Do Not Use in Production')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f" * Serving BevyFrame app '{self.package}'")
        if debug or self.debug:
            self.debug = True
        print(f" * Debug mode: {'on' if self.debug else 'off'}")
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f" * Running on http://{host}:{port}")
        print()
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"(   ) {client_address[0]} [{datetime.now().strftime('%Y-%M-%d %H:%m:%S')}]", end=' ')
                raw = client_socket.recv(1024).decode()
                recv = {
                    'method': '',
                    'path': '',
                    'protocol': '',
                    'headers': {},
                    'body': '',
                    'credentials': None
                }
                for crl in range(len(raw.split('\r'))):
                    for lfl in range(len(raw.split('\r')[crl].split('\n'))):
                        line = raw.split('\r')[crl].split('\n')[lfl]
                        if crl == lfl == 0:
                            recv['method'], recv['path'], recv['protocol'] = line.split(' ')
                        else:
                            if ': ' in line:
                                recv['headers'].update({line.split(': ')[0]: line.split(': ')[1]})
                            else:
                                recv['body'] += (line + '\r\n')
                try:
                    recv['credentials'] = get_session(
                        self.secret,
                        Request(recv, self).cookies['s']
                    )
                except KeyError:
                    pass
                if recv['credentials'] is None:
                    recv['credentials'] = {
                        'email': 'Guest@hereus.net',
                        'password': ''
                    }
                if recv['credentials']['email'].split('@')[0] != 'Guest':
                    print(f"\r(   ) {recv['credentials']['email']} [{datetime.now().strftime('%Y-%M-%d %H:%m:%S')}]",
                          end=' ')
                print(f"{recv['method']} {recv['path']} {recv['protocol']}", end='', flush=True)
                try:
                    not_in_routes = True
                    if recv['path'] in self.routes:
                        not_in_routes = False
                        resp = self.routes[recv['path']]()
                    for route in self.routes:
                        if not_in_routes:
                            match, variables = match_routing(route, recv['path'])
                            not_in_routes = not match
                            if not not_in_routes:
                                resp = self.routes[route](Request(recv, self), **variables)
                    if not_in_routes:
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
                r = f"{recv['protocol']} {resp.status_code} {https_codes[resp.status_code]}\r\n"
                for header in resp.headers:
                    r += f"{header}: {resp.headers[header]}\r\n"
                r += f"\r\n"
                r = r.encode()
                if not isinstance(resp.body, bytes):
                    resp.body = resp.body.encode()
                r += resp.body
                client_socket.sendall(r)
                client_socket.close()
                print(f'\r({resp.status_code})')
        except KeyboardInterrupt:
            server_socket.close()
            print('\r  \nServer was been terminated!\n')
