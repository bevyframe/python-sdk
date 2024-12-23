from bevyframe.Objects.Context import Context
from bevyframe.Widgets.Page import Page
import importlib.util
import os


class JavaScript:
    def __init__(self, script) -> None:
        self.script = script

    def __repr__(self) -> str:
        return self.script

    def __str__(self) -> str:
        return self.script


class change_html:
    def __init__(self, tag: str, html: str) -> None:
        self.tag = tag
        self.html = html

    def __dict__(self) -> dict:
        return {self.tag: self.html}


def process_proxy(context: Context) -> dict:
    name: str = context.json['func']
    args: list = context.json['args']
    if '/' in name or '.' in name:
        return {'error': 'Illegal token'}
    if f"{name}.py" not in os.listdir('./functions/'):
        return {'error': 'Function does not exist'}
    func_spec = importlib.util.spec_from_file_location(name, f'./functions/{name}.py')
    func = importlib.util.module_from_spec(func_spec)
    func_spec.loader.exec_module(func)
    retval = getattr(func, name)(context, *args)
    print(type(retval).__name__, end='', flush=True)
    if isinstance(retval, JavaScript):
        return {'type': 'script', 'value': retval.script}
    elif isinstance(retval, change_html):
        return {'type': 'view', 'value': retval.html, 'element': retval.tag}
    elif isinstance(retval, Page):
        return {'type': 'view', 'value': retval.render(), 'element': 'body'}
    else:
        return {'type': 'return', 'value': retval}
