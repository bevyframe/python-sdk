import importlib.resources
import os


def client_side_bridge() -> str:
    # noinspection JSUnresolvedReference
    functions = importlib.resources.files('bevyframe').joinpath('Scripts/bridge.js').read_text()
    for i in os.listdir('./functions/'):
        if i.endswith('.py'):
            i = i[:-3]
            functions += " const " + i + " = (...args) => {return _bridge('" + i + "', ...args)};"
    functions = (functions
                 .replace('    ', '')
                 .replace('  ', ' ')
                 .replace('\n', '')
                 .strip())
    return functions
