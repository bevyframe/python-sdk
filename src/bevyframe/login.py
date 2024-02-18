from .protocol import get_aas, Obj
import requests
import jwt


def get_session_token(secret, email, password) -> str:
    return jwt.encode({
        'email': email,
        'password': password
    }, secret, algorithm='HS256')


def current_user(request) -> Obj:
    r = requests.post(
        f"https://{get_aas(request.email.split('@')[1])}/protocols/current_user_info",
        data={
            'current_user_username': request.email.split('@')[0],
            'current_user_password': request.password
        }
    )
    if r.status_code == 200:
        r = r.json()
        r.update({'password': request.password})
        return Obj(r)
    else:
        return Obj({})


def get_session(secret, token) -> dict:
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        pass
    except jwt.exceptions.InvalidTokenError:
        pass
    except jwt.exceptions.InvalidKeyError:
        pass
