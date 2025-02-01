import importlib.metadata
import importlib.util
import os


class JavaScript:
    def __init__(self, script: (str, object, list)) -> None:
        if isinstance(script, list):
            script = ''.join([str(i) for i in script])
        self.script: str = script

    def render(self) -> str:
        return f'<script>{self.script}</script>'

    def __repr__(self) -> str:
        return self.script

    def __str__(self) -> str:
        return self.script


class change_html:
    def __init__(self, tag: str, html) -> None:
        self.tag: str = tag
        self.html = html
        if hasattr(self.html, "render"):
            self.html = self.html.render()
        elif isinstance(self.html, list):
            l = self.html
            self.html = ''
            for html in l:
                if hasattr(html, "render"):
                    self.html += html.render()
                else:
                    self.html += html

    def __dict__(self) -> dict:
        return {self.tag: self.html}


def process_proxy(context) -> dict:
    setattr(context, 'path', context.json['path'])
    if context.headers.get('Origin', '://').split('/')[2] != context.headers.get('Host'):
        return {'error': 'cross-origin not allowed'}
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
        return {'type': 'script', 'value': str(retval.script)}
    elif isinstance(retval, change_html):
        return {'type': 'view', 'value': retval.html, 'element': retval.tag}
    elif type(retval).__name__ == 'Page':
        return {'type': 'view', 'value': retval.render(), 'element': 'body'}
    else:
        return {'type': 'return', 'value': retval}
