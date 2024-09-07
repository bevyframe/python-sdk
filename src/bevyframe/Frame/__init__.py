import importlib.metadata
import sys
from typing import Any
import getpass
import os
from bevyframe.Objects.Response import Response
import requests
from TheProtocols import *
import json
from bevyframe.Frame.error_handler import error_handler
from bevyframe.Frame.route import route
from bevyframe.Frame.default_logging import default_logging
from bevyframe.Frame.Run.Booting import booting
from bevyframe.Frame.Run.Receiver import receiver
from bevyframe.Frame.Run.Responser import responser
from bevyframe.Frame.Run.Sender import sender
from bevyframe.Frame.Run.WSGI_Receiver import wsgi_receiver
from bevyframe.Features.Style import compile_object as compile_style
from bevyframe.Helpers.Identifiers import https_codes
from bevyframe.Features.Database import Database
import logging


class Frame:
    def __init__(
            self,
            package,
            developer,
            administrator,
            secret,
            permissions,
            style,
            icon='/favicon.ico',
            keywords=None,
            default_network='hereus.net',
            loginview='Login.py',
            environment=None,
            cors=False,
            did=None
    ) -> None:
        if keywords is None:
            keywords = []
        self.cors = cors
        self.environment = environment if environment else {}
        self.loginview = loginview
        self.default_network = default_network
        self.secret = secret
        self.package = package
        self.debug = False
        self.developer = developer
        self.routes = {}
        self.tp_token = None
        self.tp = TheProtocols(
            package,
            permissions,
            secure=False
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
        self.keywords = keywords
        self.default_logging_str = None
        self.db: (Database, None) = None
        if did:
            self.route('/.well-known/atproto-did')(lambda request: Response(
                body=did,
                credentials={},
                headers={'content_type': 'plain/text'},
                status_code=200,
                app=self
            ))
        self.__wsgi_server = None if sys.argv[0].endswith('.py') else sys.argv[0].split("/")[-1]
        if self.__wsgi_server:
            print(f"Taking control from {self.__wsgi_server}...")
            print()
            print(f"BevyFrame {importlib.metadata.version('bevyframe')} ⍺")
            print(f" * Serving BevyFrame app '{self.package}'")
            print(f" * Mode: wsgi")
            # noinspection HttpUrlsUsage
            print(f" * Running via {sys.argv[0].split('/')[-1]}")
        print()

    def error_handler(self, request, status_code, exception) -> Response:
        return error_handler(self, request, status_code, exception)

    def route(self, path, whitelist: list = None, blacklist: list = None) -> Any:
        return route(self, path, whitelist, blacklist)

    def default_logging(self, func):
        return default_logging(self, func)

    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = False):
        server_socket = booting(self, host, port, debug)
        try:
            while True:
                recv, client_socket, req_time, r, display_status_code = receiver(self, server_socket)
                resp, display_status_code = responser(self, recv, req_time, r, display_status_code)
                sender(self, recv, resp, client_socket, display_status_code)
        except KeyboardInterrupt:
            server_socket.close()
            print('\r  \nServer was been terminated!\n')

    def __call__(self, environ, start_response):
        self.debug = False
        recv, req_time, r = wsgi_receiver(self, environ)
        resp, display_status_code = responser(self, recv, req_time, r)
        start_response(f"{resp.status_code} {https_codes[resp.status_code].upper()}", [(str(i), str(resp.headers[i])) for i in resp.headers])
        print(f'\r({resp.status_code})' if display_status_code else '')
        return [resp.body.encode()]

    def __del__(self):
        if self.__wsgi_server:
            print(f"\nReturning control is back to {self.__wsgi_server}...")
