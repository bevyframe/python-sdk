import urllib.parse
from TheProtocols import *
from typing import Any
import json
import jinja2

from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page


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
            self.token = data['credentials']['token']
        except KeyError:
            self.email = 'Guest@' + app.default_network
            self.token = ''
        self._user = None
        self._data = None
        self.is_data_assigned = False
        self._preferences = None
        self.is_preferences_assigned = False
        self.app = app
        self.tp: TheProtocols = app.tp
        self.cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split('; '):
                if '=' in cookie:
                    self.cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})

    @property
    def user(self):
        if self._user is None:
            try:
                if self.email.split('@')[0] == 'Guest':
                    self._user = self.tp.create_session(f'Guest@{self.app.default_network}', '')
                else:
                    self._user = self.tp.restore_session(self.email, self.token)
            except CredentialsDidntWorked:
                self._user = self.tp.create_session(f'Guest@{self.app.default_network}', '')
            except NetworkException:
                self._user = self.tp.create_session(f'Guest@{self.app.default_network}', '')
        return self._user

    def get_data(self) -> dict:
        if self._data is None:
            self._data = self.user.data()
        return self._data

    def set_data(self, data: dict) -> None:
        self.is_data_assigned = True
        self._data = data

    # noinspection PyTypeChecker
    data = property(get_data, set_data)

    def render_template(self, template: str, **kwargs) -> str:
        with open(template.removeprefix('/')) as f:
            return jinja2.Template(f.read()).render(request=self, style=f"<style>{self.app.style}</style>", **kwargs)

    def create_response(
            self,
            body: (Page, str, dict, list) = '',
            credentials: dict = None,
            headers: dict = None,
            status_code: int = 200
    ) -> Response:
        return Response(
            body,
            headers=headers if headers is not None else {'Content-Type': 'text/html; charset=utf-8'},
            credentials=credentials if credentials is not None else {'email': self.email, 'token': self.token},
            status_code=status_code,
            app=self.app
        )

    def start_redirect(self, to_url) -> Response:
        return self.create_response(
            headers={'Location': to_url},
            status_code=303,
            credentials={'email': self.email, 'token': self.token}
        )

    @property
    def json(self) -> Any:
        return json.loads(self.body)
