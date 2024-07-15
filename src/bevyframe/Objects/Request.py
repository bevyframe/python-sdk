import urllib.parse
import TheProtocols
from TheProtocols.Data import DataRoot
from typing import Any
import json


class Request:
    def __init__(self, data: dict[str], app) -> None:
        self.method = data['method']
        self.path = data['path']
        self.headers = data['headers']
        self.query = data['query']
        self.body = urllib.parse.unquote(data['body'].replace('+', ' '))
        self.form = {}
        for b in self.body.split('\r\n'):
            for i in b.split('&'):
                if '=' in i:
                    self.form.update({i.split('=')[0]: i.split('=')[1]})
        try:
            self.email = data['credentials']['email']
            self.password = data['credentials']['password']
            try:
                self.user = TheProtocols.ID(self.email, self.password)
            except TheProtocols.CredentialsDidntWorked:
                self.user = TheProtocols.ID(f'Guest@{app.default_network}', '')
            self.data = DataRoot(self.user, app.package)()
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
