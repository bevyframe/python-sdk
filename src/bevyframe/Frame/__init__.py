import importlib.metadata
import sys
import os
from datetime import datetime

from bevyframe.Features.Login import get_session
from bevyframe.Objects.Context import Context
from bevyframe.Objects.Response import Response
import requests
import json
import time
from bevyframe.Features.Style import compile_object as compile_style
from bevyframe.Helpers.Identifiers import https_codes
from bevyframe.Frame.error_handler import error_handler
from bevyframe.Frame.route import route
from bevyframe.Frame.Responser import responser
from bevyframe.Frame.default_logging import default_logging
from TheProtocols.theprotocols import TheProtocols
from bevyframe.Frame.wsgi_runner import make_server


class Frame:
    def __init__(
            self,
            package: str,
            secret: str,
            permissions: list[str],
            style: any,
            icon: str = '/favicon.ico',
            default_network: str = 'hereus.net',
            loginview='Login.py',
            environment: (dict, callable) = None,
            cors: bool = False,
            disable_features: list[str] = False,
    ) -> None:
        self.disabled = disable_features
        self.vars = {}
        self.cors = cors
        self.environment = environment if environment else {}
        self.loginview = loginview
        self.default_network = default_network
        self.secret = secret
        self.package = package
        self.debug = False
        self.routes = {}
        self.tp_token = None
        if 'TheProtocols' not in self.disabled:
            self.tp = TheProtocols(
                package,
                permissions
            )
        else:
            self.tp = None
        if isinstance(style, str):
            if os.path.isfile(style):
                self.style = json.load(open(style, 'rb'))
            elif style.startswith('https://'):
                r = requests.get(style)
                if r.status_code == 200:
                    if r.headers['Content-Type'] == 'application/json':
                        self.style = r.json()
                    else:
                        self.style = r.content.decode()
                else:
                    self.style = {}
            else:
                self.style = style
        else:
            self.style = style
        self.style = compile_style(self.style)
        self.icon = icon
        self.default_logging_str = None
        self.db = None
        self.__wsgi_server = None if sys.argv[0].endswith('.py') else sys.argv[0].split("/")[-1]
        if sys.argv[0].split('/')[-1] == 'bevyframe':
            self.__wsgi_server = None
        if self.__wsgi_server:
            print(f"Taking control from {self.__wsgi_server}...")
            print()
            print(f"BevyFrame {importlib.metadata.version('bevyframe')} ⍺")
            print(f" * Serving BevyFrame app '{self.package}'")
            print(f" * Mode: wsgi")
            # noinspection HttpUrlsUsage
            print(f" * Running via {sys.argv[0].split('/')[-1]}")
        print()

    def error_handler(self, request: Context, status_code: int, exception: str) -> Response:
        return error_handler(self, request, status_code, exception)

    def route(self, path: str, whitelist: list = None, blacklist: list = None) -> any:
        return route(self, path, whitelist, blacklist)

    def default_logging(self, func: callable) -> callable:
        if 'CustomLogging' in self.disabled:
            return lambda: func()
        return default_logging(self, func)

    @property
    def reverse_routes(self) -> dict[str, str]:
        return {self.routes[i]: i for i in self.routes}

    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = False):
        with make_server(self, host, port) as server:
            try:
                print(f"BevyFrame {importlib.metadata.version('bevyframe')} ⍺")
                print('Development server, do not use in production deployment')
                print(f" * Serving BevyFrame app '{self.package}'")
                if debug or self.debug:
                    self.debug = True
                print(f" * Mode: {'debug' if self.debug else 'test'}")
                # noinspection HttpUrlsUsage
                print(f" * Running on http://{host}:{port}/".replace(":80/", "/").replace('://0.0.0.0', '://localhost'))
                print()
                server.serve_forever()
            except KeyboardInterrupt:
                print('\r  \nServer was been terminated!\n')

    def __call__(self, environ: dict, start_response: callable) -> list[bytes]:
        if self.__wsgi_server:
            self.debug = False
        req_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        recv = {
            'method': environ['REQUEST_METHOD'],
            'path': environ['PATH_INFO'],
            'protocol': environ.get('SERVER_PROTOCOL', 'http/1.1'),
            'headers': {},
            'body': environ['wsgi.input'].read() if 'wsgi.input' in environ else b'',
            'credentials': {},
            'query': environ.get('QUERY_STRING', ''),
            'ip': environ.get('REMOTE_ADDR', '0.0.0.0')
        }
        for header in environ:
            if header.startswith('HTTP_'):
                key = header[5:].removeprefix('HTTP_').replace('_', '-').title()
                recv['headers'].update({key: environ[header]})
        recv['credentials'] = get_session(
            self.secret,
            recv['headers'].get('Cookie', 's=').removesuffix(';').split(';').pop().split('s=')[1]
        ) if 's=' in recv['headers'].get('Cookie', 's=') else None
        r = Context(recv, self)
        display_status_code = True
        id_on_log = r.ip if r.email.split('@')[0] == 'Guest' else r.email
        if r.path == '/.well-known/bevyframe/proxy':
            recv['log'] = f"(   ) {id_on_log} [{req_time}] {r.json['func']}({', '.join([repr(i) for i in r.json['args']])}) -> "
        elif r.path == '/.well-known/bevyframe/pwa.webmanifest' and 'PWA' not in self.disabled:
            recv['log'] = f"(   ) {id_on_log} [{req_time}] GET PWA Manifest"
        elif self.default_logging_str is None:
            recv['log'] = f"(   ) {id_on_log} [{req_time}] {r.method} {r.path}"
        else:
            formatted_log = self.default_logging_str(r, req_time)
            if isinstance(formatted_log, tuple):
                formatted_log, display_status_code = formatted_log
            formatted_log = formatted_log.replace('\n', '').replace('\r', '')
            recv['log'] = ('(   ) ' if display_status_code else '      ') + formatted_log
        print(recv['log'], end='', flush=True)
        resp, display_status_code = responser(self, recv, req_time, r, display_status_code)
        if callable(resp):
            def _start_response(status, headers) -> callable:
                print(f'\r({status.split(" ", 1)[0]})' if display_status_code else '')
                return start_response(status, headers)
            return resp(environ, _start_response)
        start_response(f"{resp.status_code} {https_codes[resp.status_code].upper()}", [(str(i), str(resp.headers[i])) for i in resp.headers])
        print(f'\r({resp.status_code})' if display_status_code else '')
        if isinstance(resp.body, bytes):
            return [resp.body]
        else:
            return [resp.body.encode()]

    def __del__(self) -> None:
        if self.__wsgi_server:
            print(f"\nReturning control is back to {self.__wsgi_server}...")
