import os
import secrets
import sys


def cmdline():
    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage: python -m bevyframe <path to project>")
        sys.exit(1)
    elif args[0] == "init":
        with open('src/main.py', 'w') as f:
            f.write(f'''
from bevyframe import *

app = Frame(
    package="{input("Package: ")}",
    developer="{input("Developer: ")}",
    administrator=False,
    secret="{secrets.token_hex(secrets.randbits(6))}",
    style="{input("Style Path/URL: ")}",
    icon="{input("Icon Path/URL: ")}",
    keywords=[],
    default_network="{input("Default Network: ")}",
    loginview='Login.py'
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
            '''.removeprefix('\n'))
        print('Creating / page.', end=' ', flush=True)
        os.system('bevyframe new /')
    elif args[0] == "new":
        with open(f'src/{args[1].removeprefix("/").removesuffix("/")}' + ('' if args[1].endswith('.py') else '/__init__.py'), 'w') as f:
            f.write(f'''
from bevyframe import *


def get(r: Request) -> Page:
    return Page(
        title="{input("Title: ")}",
        selector=f'body_{"{r.user.id.settings.theme_color}"}',
        childs=[
            # Place Navbar above Root,
            Root([
                # Place your content here
            ])
        ]
    )
        '''.removeprefix('\n'))
