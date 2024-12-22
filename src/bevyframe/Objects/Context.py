import urllib.parse

from TheProtocols import *
from typing import Any, Callable
import json
import jinja2

from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page
from bevyframe.Helpers.LazyInitDict import LazyInitDict


def lazy_init_data(con) -> Callable[[Any], None]:
    def initialize(self) -> None:
        self._data = con.user.data()
    return initialize


def lazy_init_pref(con) -> Callable[[Any], None]:
    def initialize(self) -> None:
        self._data = con.user.preferences()
    return initialize


class Context:

    def __init__(self, data: dict, app) -> None:
        self.method = data['method']
        self.path = data['path'].split('?')[0]
        self.headers = data['headers']
        self.ip = data.get('ip', '127.0.0.1')
        self.query = {}
        self.env = app.environment() if callable(app.environment) else app.environment
        if not isinstance(self.env, dict):
            self.env = {}
        self.tp = app.tp
        while data['body'].endswith('\r\n'):
            data['body'] = data['body'].removesuffix('\r\n')
        while data['body'].startswith('\r\n'):
            data['body'] = data['body'].removeprefix('\r\n')
        self.body = urllib.parse.unquote(data['body'].replace('+', ' '))
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
            self.token = data['credentials'].get('token', None)
            self.password = data['credentials'].get('password', None)
        except KeyError:
            self.email = 'Guest@' + app.default_network
            self.token = ''
        self._user = None
        self.data = LazyInitDict(lazy_init_data(self))
        self.preferences = LazyInitDict(lazy_init_pref(self))
        self.app = app
        self.tp: TheProtocols = app.tp
        self.cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split('; '):
                if '=' in cookie:
                    self.cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})

    @property
    def user(self) -> Session:
        if self._user is None:
            try:
                if self.email.split('@')[0] == 'Guest':
                    self._user = self.tp.create_session(f'Guest@{self.app.default_network}', '')
                elif self.token:
                    self._user = self.tp.restore_session(self.email, self.token)
                else:
                    self._user = self.tp.create_session(self.email, self.password)
            except CredentialsDidntWorked:
                self._user = self.tp.create_session(f'Guest@{self.app.default_network}', '')
            except NetworkException:
                self._user = self.tp.create_session(f'Guest@{self.app.default_network}', '')
        return self._user

    def render_template(self, template: str, **kwargs) -> str:
        with open("./pages/" + template.removeprefix('/')) as f:
            return jinja2.Template(f.read()).render(request=self, style=f"<style>{self.app.style}</style>", **kwargs)

    def create_response(
            self,
            body: (Page, str, dict, list) = '',
            credentials: dict = None,
            headers: dict = None,
            status_code: int = 200
    ) -> Response:
        if credentials is None:
            credentials = {'email': self.email, 'token': self.token}
        if credentials['token'] is None:
            credentials = {'email': self.email, 'password': self.password}
        return Response(
            body,
            headers=headers if headers is not None else {'Content-Type': 'text/html; charset=utf-8'},
            credentials=credentials,
            status_code=status_code,
            app=self.app
        )

    def start_redirect(self, to_url) -> Response:
        return self.create_response(
            headers={'Location': to_url},
            status_code=303,
            credentials={'email': self.email, 'token': self.token}
        )

    @staticmethod
    def get_asset(path: str) -> str:
        return "/assets/" + path

    @property
    def json(self) -> Any:
        return json.loads(self.body)
