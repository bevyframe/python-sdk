import importlib.metadata
import json
import os
import random
import socket
import subprocess
import sys
import psutil
import webview
import webview.menu as wm
from bevyframe.cmdline import build_frame

sys.argv[0] = 'bevyframe'
frame = build_frame([])[0]
frame.default_logging(lambda _1, _2: ('', False))


def application(wv_env, wv_sr) -> list[bytes]:
    def start_response(status_line, response_headers: list[tuple[str, str]]) -> None:
        for k, v in response_headers:
            if k == 'Set-Cookie':
                with open(f'{app_folder}/Cookie.txt', 'w') as cookie:
                    cookie.write(v)
        return wv_sr(status_line, response_headers)
    if 'Library' in os.path.expanduser("~/"):
        app_folder = os.path.expanduser(f"~/Library/Application Support/{frame.package}")
    else:
        app_folder = os.path.expanduser(f"~/.config/share/{frame.package}")
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    if 'Cookie.txt' not in os.listdir(app_folder):
        with open(f'{app_folder}/Cookie.txt', 'w') as cookie:
            cookie.write('')
    with open(f'{app_folder}/Cookie.txt') as cookie:
        cookie = cookie.read()
    environ = {
        'REQUEST_METHOD': wv_env.get('REQUEST_METHOD', 'GET'),
        'PATH_INFO': wv_env.get('PATH_INFO', '/'),
        'REMOTE_ADDR': wv_env.get('REMOTE_ADDR', '127.0.0.1'),
        'QUERY_STRING': wv_env.get('QUERY_STRING', ''),
        'HTTP_USER_AGENT': wv_env.get('HTTP_USER_AGENT').split(' Chrome')[0] + f" bevyframe/{importlib.metadata.version('bevyframe')}",
        'HTTP_ACCEPT': 'text/html',
        'wsgi.input': wv_env.get('wsgi.input'),
        'HTTP_Device-Memory': int(psutil.virtual_memory().total / (1024 ** 3)),
        'HTTP_COOKIE': cookie,
    }
    for k, v in wv_env.items():
        if k.startswith('HTTP_') and k not in environ:
            environ[k] = v
    return frame(environ, start_response)


# from http.py of r0x0r/pywebview
def _get_random_port() -> int:
    while True:
        port = random.randint(1023, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('localhost', port))
            except OSError:
                continue
            else:
                return port


class Desktop:
    def __init__(self) -> None:
        with open('manifest.json') as f:
            self.manifest = json.load(f)
        self.port = _get_random_port()
        self.proc = subprocess.Popen(["gunicorn", "bevyframe.Platforms.Desktop", "-b", f"127.0.0.1:{self.port}"])
        self.window = webview.create_window(
            self.manifest['app']['name'],
            url=f"http://127.0.0.1:{self.port}/",
            min_size=(520, 390)
        )
        self.menu = []  # WORK ON THIS

    def start(self) -> int:
        webview.start(
            menu=self.menu,
            icon=f"./{self.manifest['app']['icon']}",
        )
        self.proc.kill()
        return 0
