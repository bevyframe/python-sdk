from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import hmac
import json
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


def get_session_token(secret: bytes, email: str, token: str = None) -> str:
    data = json.dumps({'email': email, 'token': token}).encode()
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES256(secret), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv.hex() + ':' + ciphertext.hex() + ':' + encryptor.tag.hex()


def get_session(secret: bytes, token: str) -> dict:
    # noinspection PyBroadException
    try:
        iv, ciphertext, tag = token.split(':')
        iv = bytes.fromhex(iv)
        ciphertext = bytes.fromhex(ciphertext)
        tag = bytes.fromhex(tag)
        cipher = Cipher(algorithms.AES(secret), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return json.loads(plaintext.decode())
    except Exception:
        return {}


def login_required(func) -> callable:
    def wrapper(r, *args, **kwargs) -> any:
        if r.email.split('@')[0] == 'Guest':
            return r.start_redirect(f"/{r.app.loginview.removeprefix('/')}")
        else:
            return func(r, *args, **kwargs)
    return wrapper
