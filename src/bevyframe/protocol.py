from typing import Any
import requests


def get_aas(domain) -> str:
    r = requests.post('https://aas.hereus.net', json={
        'domain': domain
    })
    if r.status_code == 200:
        return r.content.decode()
    else:
        return domain


class Obj:
    def __init__(self, obj) -> None:
        self.obj = obj

    def __getattr__(self, item) -> Any:
        if isinstance(self.obj[item], dict):
            return Obj(self.obj[item])
        else:
            return self.obj[item]


def library_data(app, data: dict = None):
    r = requests.post(
        f"https://{get_aas(app.administrator.network)}/protocols/" + (
            'pull_library_data' if data is None else 'push_library_data'
        ), **({} if data is None else {'data': {
            'current_user_username': app.administrator.username,
            'current_user_password': app.administrator.password,
            'app': app.package
        }})
    )
    if data is not None:
        if r.status_code == 200:
            return r.json()
        else:
            return {}


def find_user(email: str) -> dict:
    r = requests.post(
        f"https://{get_aas(email.split('@')[1])}/protocols/user_info",
        data={
            'username': email.split('@')[0]
        }
    )
    if r.status_code == 200:
        return r.json()
    else:
        return {}


def get_admin(email, password) -> dict:
    r = requests.post(
        f"https://{get_aas(email.split('@')[1])}/protocols/current_user_info",
        data={
            'current_user_username': email.split('@')[0],
            'current_user_password': password
        }
    )
    if r.status_code == 200:
        r = r.json()
        r.update({'password': password})
        return r
    else:
        return {}
