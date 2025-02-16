from TheProtocols.helpers.exceptions import CredentialsDidntWorked, NetworkException
from TheProtocols.session import Session
from bevyframe.Features.BridgeJS import client_side_bridge
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page
import urllib.parse
import jinja2
import json
import os

default_keys = [
    'method', 'path', 'headers', 'browser', 'ip', 'query',
    'env', 'tp', 'body', 'form', 'email', 'token', 'data',
    'preferences', 'app', 'cookies', 'not_locked', 'user',
    'db', 'get_asset', 'render_template', 'start_redirect',
    'create_response', 'execute', 'json',
]


def lazy_init_data(con) -> callable:
    def initialize(self) -> None:
        self._data = con.user.data()
    return initialize


def lazy_init_pref(con) -> callable:
    def initialize(self) -> None:
        self._data = con.user.preferences()
    return initialize


class Browser:
    def __init__(self, headers: dict) -> None:
        self.language = headers.get('Accept-Language', 'en-US').split(',')[0].split(';')[0].strip()
        self.ram = headers.get('Device-Memory', 0)
        self.bandwidth = headers.get('Downlink', 0)
        self.network_profile = headers.get('ECT', 'NotGiven')
        self.user_agent = ua = headers.get('User-Agent', 'Mozilla/5.0 (;) AppleWebKit/0.0 (KHTML, like Gecko) Chrome/0.0.0.0 Safari/0.0)')
        try:
            ua = ua.removeprefix(ua.split('(')[0] + '(')
            self.device = ua.split(')')[0]
            ua = ua.removeprefix(self.device + ')').removeprefix(' AppleWebKit/')
            self.webkit_version = ua.split('(')[0]
            ua = ua.split(')')[1].removeprefix(' ')
            self.name = ua.split('/')[0]
            self.version = ua.split('/')[1].split(' ')[0]
        except IndexError:
            self.device = ''
            self.os = ''
            self.webkit_version = 'NotCompatible'
            self.name = 'Hidden'
            self.version = ''


class Run:
    def __init__(self, commands: list[str]) -> None:
        self.commands = commands

    def __getattr__(self, name: str) -> callable:
        return Run(self.commands + [name])

    def __call__(self, *args) -> "Run":
        self.commands[-1] = self.commands[-1] + '(' + ', '.join(repr(arg) for arg in args) + ')'
        return self

    def __str__(self) -> str:
        return '.'.join(self.commands)

    def __repr__(self) -> str:
        return self.__str__()


class Context:
    def __init__(self, data: dict, app) -> None:
        self.not_locked = True
        self.app = app
        self.method = data['method']
        self.path = data['path'].split('?')[0]
        self.headers = data['headers']
        self.browser = Browser(self.headers)
        self.ip = data.get('ip', '127.0.0.1')
        if self.ip == '127.0.0.1':
            if 'X-Forwarded-For' in self.headers:
                self.ip = self.headers['X-Forwarded-For']
            elif 'X-Real-Ip' in self.headers:
                self.ip = self.headers['X-Real-Ip']
        self.query = {}
        self.env = app.environment() if callable(app.environment) else app.environment
        if not isinstance(self.env, dict):
            self.env = {}
        self.tp = app.tp
        try:
            data['body'] = data.get('body', b'').decode()
        except UnicodeDecodeError:
            pass
        if isinstance(data['body'], str):
            while data['body'].endswith('\r\n'):
                data['body'] = data['body'].removesuffix('\r\n')
            while data['body'].startswith('\r\n'):
                data['body'] = data['body'].removeprefix('\r\n')
        self.body = data['body']
        self._json = {}
        self._form = {}
        if 'UserContext' in self.app.disabled:
            self._user = None
        if data['query']:
            for i in data['query'].split('&'):
                if '=' in i:
                    self.query.update({
                        urllib.parse.unquote(i.split('=')[0].replace('+', ' ')): urllib.parse.unquote(i.split('=')[1].replace('+', ' '))
                    })
                else:
                    self.query.update({
                        urllib.parse.unquote(i): True
                    })
        self.email = data['credentials'].get('email', f"Guest@{app.default_network}")
        self.token = data['credentials'].get('token', '')
        if 'TheProtocols' not in self.app.disabled:
            from bevyframe.Helpers.LazyInitDict import LazyInitDict
            self.data = LazyInitDict(lazy_init_data(self))
            self.preferences = LazyInitDict(lazy_init_pref(self))
        else:
            self.data = None
            self.preferences = None
        self.cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split('; '):
                if '=' in cookie:
                    self.cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})
        self.not_locked = False

    # noinspection PyMissingTypeHints
    @property
    def db(self):
        return self.app.db

    @property
    def execute(self) -> Run:
        return Run([])

    # noinspection PyAttributeOutsideInit
    @property
    def user(self) -> (Session, None):
        if 'TheProtocols' in self.app.disabled:
            return None
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

    def render_template(self, template: str, **kwargs) -> (Response, str):
        with open("./pages/" + template.removeprefix('/')) as f:
            html = f.read()
            if '<body' in html:
                prop = html.split('<body')[1].split('>')[0].split(' ')
                for i in prop:
                    if i.split('=')[0] == 'login_required' and self.email.split('@')[0] == 'Guest':
                        return self.start_redirect(f"/{self.app.loginview.removeprefix('/')}")
            return jinja2.Template(html).render(
                context=self,
                style=f"<style>{self.app.style}</style>",
                functions=f"<script>{client_side_bridge()}</script>" if 'JsBridge' not in self.app.disabled else "",
                safe=lambda x: x.replace('<', '&lt;').replace('>', '&gt;'),
                **kwargs
            )

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
    def json(self) -> any:
        if not self._json:
            self._json = json.loads(self.body)
        return self._json

    @property
    def form(self) -> any:
        if not self._json:
            self._form = {}
            for b in self.body.split('\r\n'):
                for i in b.split('&'):
                    if '=' in i:
                        self._form.update({
                            urllib.parse.unquote(i.split('=')[0].replace('+', ' ')): urllib.parse.unquote(i.split('=')[1].replace('+', ' '))
                        })
        return self._form

    def string(self, path: str, language: str = 'en') -> str:
        language = language.split('/')[-1].split('-')[0]
        if f"{language}.json" not in os.listdir('./strings/'):
            language = 'en'
        if f"{language}.json" not in os.listdir('./strings/'):
            language = os.listdir('./strings/')[0].removesuffix('.json')
        with open(f"./strings/{language}.json") as f:
            strings = json.load(f)
        parts = path.split('/')
        while parts:
            strings = strings.get(parts.pop(0), {})
            if isinstance(strings, str):
                return strings
        return str(strings)


    def __setattr__(self, name: str, value: any) -> None:
        if name in ['_json', '_form']:
            object.__setattr__(self, name, value)
        elif name == 'path' and hasattr(self, 'path') and self.path == '/.well-known/bevyframe/proxy':
            object.__setattr__(self, name, value)
        elif name in default_keys and self.not_locked:
            object.__setattr__(self, name, value)
            return
        elif 'UserContext' not in self.app.disabled:
            if self.email not in self.app.vars:
                self.app.vars[self.email] = {}
            return self.app.vars[self.email].update({name: value})
        return object.__setattr__(self, name, value)

    def __getattr__(self, name: str) -> any:
        if name == 'app':
            try:
                return object.__getattribute__(self, 'app')
            except AttributeError:
                return type('Frame', (), {'disabled': ['UserContext']})()
        if 'UserContext' not in self.app.disabled:
            if name in default_keys:
                if name == 'not_locked' and 'not_locked' not in self.__dict__:
                    return True
                return object.__getattribute__(self, name)
            return self.app.vars.get(self.email, {}).get(name, None)
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name == 'not_locked':
                return True

    def __delattr__(self, name: str) -> None:
        if 'UserContext' not in self.app.disabled:
            if self.email not in self._app.vars and name in self.app.vars[self.email]:
                del self.app.vars[name]
        else:
            object.__delattr__(self, name)

    def __str__(self) -> str:
        return (f"""
Package: {self.app.package}
Cred.Email: {self.email}
Cred.Username: {self.email.split('@')[0]}
Cred.Network: {self.email.split('@')[1]}
Cred.Token: {self.token}
Path: {self.path}
IP: {self.ip}
Method: {self.method}
""" + '\n'.join([f"Header.{i}: {self.headers[i]}" for i in self.headers]) + """
        """).strip().strip('\n').strip()
