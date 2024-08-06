import urllib.parse
import TheProtocols
from TheProtocols.Data import DataRoot
from typing import Any
import json


class Request:
    def __init__(self, data: dict[str], app) -> None:
        self.method = data['method']
        self.path = data['path'].split('?')[0]
        self.headers = data['headers']
        self.query = {}
        self.env = app.environment() if callable(app.environment) else app.environment
        if not isinstance(self.env, dict):
            self.env = {}
        while data['body'].endswith('\r\n'):
            data['body'] = data['body'].removesuffix('\r\n')
        while data['body'].startswith('\r\n'):
            data['body'] = data['body'].removeprefix('\r\n')
        self.body = urllib.parse.unquote(data['body'])
        self.form = {}
        for b in data['body'].split('\r\n'):
            for i in b.split('&'):
                if '=' in i:
                    self.form.update({
                        urllib.parse.unquote(i.split('=')[0].replace('+', ' ')): urllib.parse.unquote(i.split('=')[1].replace('+', ' '))
                    })
        if '?' in data['path']:
            for i in data['path'].split('?')[1].split('&'):
                if '=' in i:
                    self.query.update({
                        urllib.parse.unquote(i.split('=')[0].replace('+', ' ')): urllib.parse.unquote(i.split('=')[1].replace('+', ' '))
                    })
                else:
                    self.query.update({
                        urllib.parse.unquote(i): True
                    })
        try:
            self.email = data['credentials']['email']
            self.password = data['credentials']['password']
            self._user = None
            self._data = None
        except TypeError:
            pass
        self.app = app
        self.cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split('; '):
                if '=' in cookie:
                    self.cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})

    @property
    def user(self):
        if self._user is None:
            try:
                self._user = TheProtocols.ID(self.email, self.password)
            except TheProtocols.CredentialsDidntWorked:
                self._user = TheProtocols.ID(f'Guest@{app.default_network}', '')
        return self._user

    @property
    def data(self) -> dict:
        if self._data is None:
            self._data = DataRoot(
                self.user,
                f"{self.app.package}{self.path.split('/')[1]}" if self.app.package.endswith('.') else self.app.package
            )()
        return self._data

    def is_data_assigned(self) -> bool:
        return self._data is not None

    @property
    def json(self) -> Any:
        return json.loads(self.body)
