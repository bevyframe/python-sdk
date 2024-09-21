from bevyframe.Widgets.Page import Page
from TheProtocols import *


class Response:
    def __init__(self, body: (Page, str, dict, list), credentials, headers, status_code, app) -> None:
        self.body = body
        self.credentials = credentials
        self.headers = headers
        self.status_code = status_code
        self.app = app
        if app is not None:
            self.tp: TheProtocols = app.tp
        else:
            self.tp = None

    def login(self, email, password) -> bool:
        try:
            self.credentials = {
                'email': email,
                'token': self.tp.create_session(email, password).token
            }
            return True
        except CredentialsDidntWorked:
            return False

    def __str__(self):
        if 'Location' in self.headers:
            return f"window.location.href = '{self.headers['Location']}'"
        else:
            return self.__repr__()
