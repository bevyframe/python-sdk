import jwt


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
