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


def dispatcher(manifest: dict, apps: dict[str, callable], path: str) -> callable:
    def app(environ, start_response) -> list[bytes]:
        host = environ['HTTP_HOST']
        if host in manifest['domains']:
            os.chdir(f"{path}/{manifest['domains'][host]}")
            ret = apps[manifest['domains'][host]](environ, start_response)
            os.chdir(path)
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
    reverse_domains = [manifest['domains'][i] for i in manifest['domains']]
    for app in reverse_domains:
        if not app.startswith('__') and os.path.isdir(app):
            os.chdir(f"{path}/{app}")
            sys.path.insert(0, f"{path}/{app}")
            apps[app] = build_frame([])[0]
            sys.path.remove(f"{path}/{app}")
            os.chdir(path)
    application = dispatcher(manifest, apps, path)
else:
    application = string_return("Manifest not found")
