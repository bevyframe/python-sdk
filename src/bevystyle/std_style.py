from bevystyle.Style import *
import importlib.util
import sys


def main() -> int:
    module_name = sys.argv[1]

    page_script_spec = importlib.util.find_spec(module_name)
    page_script = importlib.util.module_from_spec(page_script_spec)
    page_script_spec.loader.exec_module(page_script)

    compiled = compile_object(page_script)
    css = RenderCSS(compiled)
    print(css)
    return 0
