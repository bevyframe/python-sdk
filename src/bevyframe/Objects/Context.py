import markupsafe
from TheProtocols import TheProtocols
from TheProtocols.helpers.exceptions import CredentialsDidntWorked, NetworkException

from bevyframe.Features.ContextManager import get_from_context_manager, set_to_context_manager
from bevyframe.Features.ErrorHandler import Error401
from TheProtocols.session import Session
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page
import urllib.parse
import jinja2
from datetime import datetime, UTC
import json
import os

default_keys = [
    'method', 'path', 'headers', 'browser', 'ip', 'query',
    'env', 'tp', 'body', 'form', 'email', 'token', 'data',
    'preferences', 'app', 'cookies', 'not_locked', 'user',
    'db', 'get_asset', 'render_template', 'start_redirect',
    'create_response', 'execute', 'username', 'loginview',
    'json', 'network'
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
    def __init__(self, data: dict) -> None:
        self.not_locked = True
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
        self.query = data['query']
        self.tp = TheProtocols(
            data['package'],
            data['permissions'],
        )
        self.loginview = data['loginview']
        try:
            data['body'] = data.get('body', b'').decode()
            while data['body'].endswith('\r') or \
                    data['body'].endswith('\n') or \
                    data['body'].startswith('\r') or \
                    data['body'].startswith('\n'):
                data['body'] = data['body'].strip('\n')
                data['body'] = data['body'].strip('\r')
        except UnicodeDecodeError:
            pass
        self.body = data['body']
        self._json = {}
        self._form = {}
        self._user = None
        self.email = data['credentials'].get('email', f"Guest@localhost")
        self.token = data['credentials'].get('token', '')
        self.username = data['credentials'].get('username', '')
        self.network = data['credentials'].get('network', '')
        from bevyframe.Features.LazyInitDict import LazyInitDict
        self.data = LazyInitDict(lazy_init_data(self))
        self.preferences = LazyInitDict(lazy_init_pref(self))
        self.cookies = {}
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split('; '):
                if '=' in cookie:
                    self.cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})
        self.not_locked = False

    @property
    def execute(self) -> Run:
        return Run([])

    # noinspection PyAttributeOutsideInit
    @property
    def user(self) -> (Session, None):
        if self._user is None:
            try:
                self._user = self.tp.restore_session(self.email, self.token)
            except CredentialsDidntWorked:
                raise Error401
            except NetworkException:
                raise Error401
        return self._user

    def render_template(self, template: str, login_req: bool = False, **kwargs) -> (bool, str):
        if template.startswith('<!DOCTYPE html>'):
            html = template
        else:
            with open(template) as f:
                html = f.read()
        if "login-required" in html.split("<body ", 1)[-1].split('>', 1)[0].split(" "):
            login_req = True
        if login_req and self.email.split('@')[0] == 'Guest':
            return False
        return jinja2.Template(html).render(
            context=self,
            safe=markupsafe.escape,
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
        return Response(
            body,
            headers=headers if headers is not None else {'Content-Type': 'text/html; charset=utf-8'},
            credentials=credentials,
            status_code=status_code,
            context=self
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
        if not self._form:
            self._form = {}
            for i in self.body.split('&'):
                if '=' in i:
                    self._form.update({
                        urllib.parse.unquote(
                            i.split('=', 1)[0]
                            .replace('+', ' ')
                        ):
                            urllib.parse.unquote(
                                i.split('=', 1)[1]
                                .replace('+', ' ')
                            )
                    })
        return self._form

    @staticmethod
    def string(path: str, language: str = 'en') -> str:
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
        if isinstance(strings, dict):
            return f"@{language}/{path}"
        return str(strings)

    """def __setattr__(self, name: str, value: any) -> None:
        if name in ['_json', '_form', '_user']:
            object.__setattr__(self, name, value)
            return
        elif name == 'path' and hasattr(self, 'path') and self.path == '/.well-known/bevyframe/proxy':
            object.__setattr__(self, name, value)
            return
        elif name in default_keys and self.not_locked:
            object.__setattr__(self, name, value)
            return
        set_to_context_manager(self.tp.package_name, self.email, name, value)
        return

    def __getattr__(self, name: str) -> any:
        if name == 'app':
            try:
                return object.__getattribute__(self, 'app')
            except AttributeError:
                return type('Frame', (), {})()
        if name in default_keys:
            if name == 'not_locked' and 'not_locked' not in self.__dict__:
                return True
            return object.__getattribute__(self, name)
        return get_from_context_manager(self.tp.package_name, self.email, name)"""

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
Header.Date: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}
""" + '\n'.join([f"Header.{i}: {self.headers[i]}" for i in self.headers]) + """
        """).strip().strip('\n').strip()
