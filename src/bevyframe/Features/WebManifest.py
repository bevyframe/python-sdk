from bevyframe.Objects.Context import Context
import mimetypes
import json


def icon_manifest(path: str) -> dict:
    return {
        "src": path,
        "type": mimetypes.types_map.get(f".{path}", 'image/png')
    }


def web_manifest() -> dict:
    with open('./manifest.json') as f:
        manifest = json.load(f)
    return {
        "name": manifest['app']['name'],
        "short_name": manifest['app']['short_name'],
        "description": manifest['publishing']['description'],
        "start_url": "/",
        "scope": "/",
        "id": manifest['app']['package'],
        "display": "standalone",
        "orientation": manifest['app']['orientation'],
        "icons": [icon_manifest(manifest['app']['icon'])],
        "shortcuts": [{"name": manifest['app']['shortcuts'][shortcut], "url": shortcut} for shortcut in manifest['app']['shortcuts']],
        "screenshots": [icon_manifest(icon) for icon in manifest['publishing']['screenshots']],
        "display_override": ["window-controls-overlay", "minimal-ui"],
        "launch_handler": {"client_mode": "navigate-new" if manifest['app']['allow_multiple_instance'] else "navigate-existing"},
        "share_target": {
            "action": manifest['app']['shareview'],
            "method": "POST",
            "enctype": "multipart/form-data",
            "params": {
                "title": "title",
                "text": "text",
                "url": "link",
                "files": [{"name": "media", "accept": manifest['app']['accept_media']}]
            }
        }
    }
