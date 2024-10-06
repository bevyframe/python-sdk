import jwt


def get_session_token(secret, email, token=None, password=None) -> str:
    return jwt.encode({
        'email': email,
        'token': token
    } if token is not None else {
        'email': email,
        'password': password
    }, secret, algorithm='HS256')


def get_session(secret, token) -> (dict, None):
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        return None


def login_required(func):
    def wrapper(r, *args, **kwargs):
        if r.email.split('@')[0] == 'Guest':
            return r.start_redirect(f"/{r.app.loginview.removeprefix('/')}")
        else:
            return func(r, *args, **kwargs)
    return wrapper
