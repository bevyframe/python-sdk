import jwt
from bevyframe.Objects.Response import redirect


def get_session_token(secret, email, password) -> str:
    return jwt.encode({
        'email': email,
        'password': password
    }, secret, algorithm='HS256')


def get_session(secret, token) -> dict:
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except:
        return None


def login_required(func):
    def wrapper(r):
        if r.email.split('@')[0] == 'Guest':
            return redirect(f"/{r.app.loginview.removeprefix('/')}")
        else:
            return func(r)
    return wrapper
