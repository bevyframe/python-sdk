from bevyframe.Widgets.Page import Page


class Response:
    def __init__(self, body: (Page, str, dict, list), **others) -> None:
        self.body = body
        self.credentials = {}
        self.headers = {'Content-Type': 'text/html; charset=utf-8'}
        self.status_code = 200
        for kwarg in others:
            setattr(self, kwarg, others[kwarg])

    def login(self, email, password) -> None:
        self.credentials = {'email': email, 'password': password}


def redirect(to_url) -> Response:
    return Response('', headers={'Location': to_url}, status_code=303)
