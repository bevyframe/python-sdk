import hashlib
import base64
import hmac
import time
import jwt
import os


class totp:
    @staticmethod
    def create_secret() -> str:
        return base64.b32encode(os.urandom(30)).decode()

    @staticmethod
    def generate(secret: str) -> str:
        key = base64.b32decode(secret, casefold=True)
        counter = int(time.time() // 30)
        counter_bytes = counter.to_bytes(8)
        hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        offset = hmac_hash[-1] & 0x0F
        code = (hmac_hash[offset] & 0x7F) << 24 | \
               (hmac_hash[offset + 1] & 0xFF) << 16 | \
               (hmac_hash[offset + 2] & 0xFF) << 8 | \
               (hmac_hash[offset + 3] & 0xFF)
        otp = code % (10 ** 6)
        return f"{otp:0{6}}"

    @staticmethod
    def verify(secret: str, code: str) -> bool:
        for offset in range(-1, 2):
            return totp.generate(secret) == code
        return False


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
