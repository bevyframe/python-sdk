import json
import sys
from bevyframe.cmdline import build_frame
import os


def string_return(text: str) -> callable:
    def app(_, start_response) -> list[bytes]:
        b, l = text.encode(), str(len(text))
        start_response("500 Internal Server Error", [("Content-Type", "text/plain"), ("Content-Length", l)])
        return [b]
    return app


def dispatcher(manifest: dict, apps: dict[str, callable]) -> callable:
    def app(environ, start_response) -> list[bytes]:
        host = environ['HTTP_HOST']
        if host in manifest['domains']:
            os.chdir(manifest['domains'][host])
            ret = apps[manifest['domains'][host]](environ, start_response)
            os.chdir('..')
            return ret
        else:
            return string_return(f"'{host}' not found")(environ, start_response)
    return app


if 'manifest.json' in os.listdir():
    application = build_frame([])[0]
elif 'dispatcher.json' in os.listdir():
    with open('dispatcher.json') as f:
        manifest = json.load(f)
    apps = {}
    path = os.getcwd()
    for app in os.listdir():
        if not app.startswith('__') and os.path.isdir(app):
            os.chdir(app)
            sys.path.insert(0, os.getcwd())
            apps[app] = build_frame([])[0]
            sys.path.remove(os.getcwd())
            os.chdir("..")
    application = dispatcher(manifest, apps)
else:
    application = string_return("Manifest not found")
