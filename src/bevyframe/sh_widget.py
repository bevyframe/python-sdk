from bevyframe.Widgets.Widget import RenderHTML
import sys


def main() -> int:
    args, kwargs = [], {}
    raw = sys.argv[2:]
    while raw:
        arg = raw.pop(0)
        if arg.startswith("--") and len(raw) >= 1:
            kwargs[arg.removeprefix('--')] = raw.pop(0)
        else:
            args.append(arg)
    if sys.argv[1] in globals():
        print(RenderHTML(*globals()[sys.argv[1]](*args, **kwargs).bf_widget()))
    else:
        print("Widget not found")
    return 0
