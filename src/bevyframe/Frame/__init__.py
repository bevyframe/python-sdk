from typing import Any
import getpass
import os
from bevyframe.Objects.Response import Response
import requests
import TheProtocols
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


class Frame:
    def __init__(
            self,
            package,
            developer,
            administrator,
            secret,
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
        if did:
            self.route('/.well-known/atproto-did')(lambda request: Response(body=did, content_type='plain/text'))
        if administrator:
            self.admin = TheProtocols.ID(administrator, getpass.getpass(f'Password for {administrator}: '))
            print()
            print(f"Welcome {self.admin.id}!")
        print()

    def error_handler(self, request, status_code, exception) -> Response:
        return error_handler(self, request, status_code, exception)

    def route(self, path, whitelist: list = None, blacklist: list = None) -> Any:
        return route(self, path, whitelist, blacklist)

    def default_logging(self, func):
        return default_logging(self, func)

    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
        server_socket = booting(self, host, port, debug)
        try:
            while True:
                recv, client_socket, req_time, r = receiver(self, server_socket)
                resp = responser(self, recv, req_time, r)
                sender(self, recv, resp, client_socket)
        except KeyboardInterrupt:
            server_socket.close()
            print('\r  \nServer was been terminated!\n')

    def __call__(self, environ, start_response):
        debug_ = self.debug
        self.debug = False
        recv, req_time, r = wsgi_receiver(self, environ)
        resp = responser(self, recv, req_time, r)
        start_response(f"{resp.status_code} {https_codes[resp.status_code].upper()}", [(str(i), str(resp.headers[i])) for i in resp.headers])
        print(f'\r({resp.status_code})')
        self.debug = debug_
        return [resp.body.encode()]
