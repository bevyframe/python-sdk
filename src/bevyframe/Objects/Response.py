from bevyframe.Widgets.Page import Page
from TheProtocols import *


class Activity:
    def __init__(self, **kwargs) -> None:
        self.properties = kwargs
        self.context = []

    def add_context(self, item: (str, dict)) -> None:
        self.context.append(item)

    def remove_context(self, item: (str, dict)) -> None:
        self.context.remove(item)

    def bf_widget(self) -> dict:
        d = {"@context": ["https://www.w3.org/ns/activitystreams"] + self.context}
        d.update(self.properties)
        return d


class Response:
    def __init__(self, body: (Page, str, dict, list), credentials: dict[str, str], headers: dict[str, str], status_code: int, context) -> None:
        self.body = body
        self.credentials = credentials
        self.headers = headers
        self.status_code = status_code
        self.context = context
        if context is not None:
            self.tp = context.tp
        else:
            self.tp = None

    def login(self, email: str, password: str) -> bool:
        try:
            s = self.tp.create_session(email, password)
            if not hasattr(s, 'token'):
                return False
            if s.token is None:
                return False
            self.credentials = {
                'email': email,
                'token': s.token
            }
            return True
        except CredentialsDidntWorked:
            return False

    def __str__(self) -> str:
        if 'Location' in self.headers:
            return f"window.location.href = '{self.headers['Location']}'"
        else:
            return repr(self)
