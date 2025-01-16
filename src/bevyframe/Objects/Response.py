from bevyframe.Widgets.Page import Page
from TheProtocols import *


class Response:
    def __init__(self, body: (Page, str, dict, list), credentials: dict[str, str], headers: dict[str, str], status_code: int, app) -> None:
        self.body = body
        self.credentials = credentials
        self.headers = headers
        self.status_code = status_code
        self.app = app
        if app is not None:
            self.tp = app.tp
        else:
            self.tp = None

    def login(self, email: str, password: str) -> bool:
        try:
            s = self.tp.create_session(email, password)
            if not hasattr(s, 'token'):
                return False
            self.credentials = {
                'email': email,
                'token': s.token
            }
            if self.credentials['token'] is None:
                return False
            return True
        except CredentialsDidntWorked:
            return False

    def __str__(self) -> str:
        if 'Location' in self.headers:
            return f"window.location.href = '{self.headers['Location']}'"
        else:
            return self.__repr__()
