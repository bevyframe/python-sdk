import importlib.resources
import json


def service_worker() -> str:
    with open('./manifest.json') as f:
        manifest = json.load(f)
    sw = importlib.resources.files('bevyframe').joinpath('Scripts/sw.js').read_text()
    return sw.replace('---offlineview---', manifest['app']['offlineview'])