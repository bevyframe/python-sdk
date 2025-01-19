import importlib.metadata
import sys
import os

from bevyframe.Objects.Context import Context
from bevyframe.Objects.Response import Response
import requests
from TheProtocols import *
import json
from bevyframe.Frame.error_handler import error_handler
from bevyframe.Frame.route import route
from bevyframe.Frame.default_logging import default_logging
from bevyframe.Frame.Run.Responser import responser
from bevyframe.Frame.Run.Receiver import receiver
from bevyframe.Features.Style import compile_object as compile_style
from bevyframe.Helpers.Identifiers import https_codes
from bevyframe.Features.Database import Database
from bevyframe.Frame.Run.wsgi_runner import make_server


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
        self.tp = TheProtocols(
            package,
            permissions
        )
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
        self.db: (Database, None) = None
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
        recv, req_time, r, display_status_code = receiver(self, environ)
        resp, display_status_code = responser(self, recv, req_time, r, display_status_code)
        if isinstance(resp, Response):
            start_response(f"{resp.status_code} {https_codes[resp.status_code].upper()}", [(str(i), str(resp.headers[i])) for i in resp.headers])
            print(f'\r({resp.status_code})' if display_status_code else '')
            if isinstance(resp.body, bytes):
                return [resp.body]
            else:
                return [resp.body.encode()]
        elif callable(resp):
            def _start_response(status, headers) -> callable:
                print(f'\r({status.split(" ", 1)[0]})' if display_status_code else '')
                return start_response(status, headers)
            return resp(environ, _start_response)

    def __del__(self) -> None:
        if self.__wsgi_server:
            print(f"\nReturning control is back to {self.__wsgi_server}...")
