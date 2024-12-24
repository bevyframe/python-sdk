from bevyframe.Frame import Frame
from bevyframe.Features.Database import Database
from bevyframe.Helpers.MainPyCompiler import MainPyCompiler as main
import json
import os
from random import randint
import sys
import importlib
import importlib.util


def init(*args) -> int:
    if os.system("which pymake > /dev/null 2>&1") != 0:
        print("ERROR: pymake is not installed")
        input("Please create your standard Python environment, then click any key...")
    else:
        print('\n', end='', flush=True)
        os.system("pymake init --no-module")
    os.system("mv ./src/ ./pages/")
    with open('.gitignore') as f:
        gitignore = f.read().splitlines()
    if '.secret' not in gitignore:
        gitignore.append(".secret")
    if '*.db' not in gitignore:
        gitignore.append("*.db")
    with open('.gitignore', 'w') as f:
        f.writelines([f"{i}\n" for i in gitignore])
    with open('.secret', 'w') as f:
        secret = ''.join([hex(randint(0, 15)).removeprefix('0x') for _ in range(128)])
        f.write(secret)
    os.mkdir('assets')
    os.mkdir('functions')
    with open('models.py', 'w') as f:
        f.write('from bevyframe import *\nBase = DeclarativeBase()\n')
    with open('README.md') as f:
        project_name = f.read().splitlines()[0].removeprefix('# ')
    manifest = {
        "@context": "https://bevyframe.islekcaganmert.me/ns/manifest",
        "app": {
            "package": input("Package: "),
            "style": input("\nStyle name or CSS URL/path: "),
            "icon": "/.assets/favicon.png",
            "loginview": "/Login.py",
            "database_filename": "app",
            "cors": False,
            "routing": {}
        },
        "accounts": {
            "default_network": input("\nDefault Network: "),
            "permissions": []
        },
        "development": {
            "host": "0.0.0.0",
            "port": 3000,
            "debug": True
        },
        "production": {
            "web": {
                "host": "0.0.0.0",
                "port": 80
            },
            "ios": False,
            "android": False,
            "nt": False,
            "macos": False,
            "snap": False,
            "flatpak": False,
            "luos": False
        },
        "requirements": [],
    }
    with open('./manifest.json', 'w') as f:
        f.write(json.dumps(manifest))
    os.remove('./requirements.txt')
    os.remove('./pages/main.py')
    os.system("bevyframe new / '" + project_name.replace('\'', '\\\'') + "'")
    frame = build_frame([])[0]
    frame.db.create_all()
    print()
    return 0


def new(*args) -> int:
    with open(f'./pages/{args[0].removeprefix("/").removesuffix("/")}' + ('' if args[0].endswith('.py') else '/__init__.py'), 'w') as f:
        f.write(f'''
from bevyframe import *


def get(r: Context) -> Page:
    return Page(
        title="{input("Title: ") if len(sys.argv) < 3 else args[1]}",
        color=r.user.id.settings.theme_color,
        childs=[
            # Place Navbar above Root,
            Root([
                # Place your content here
            ])
        ]
    )
            '''.removeprefix('\n'))
    return 0


def build_frame(*args) -> tuple[Frame, dict]:
    if 'manifest.json' not in os.listdir('./'):
        print('\nNo manifest.json found. This project is available for managed run.')
        print('Please run your app via `pymake run` or `cd src && python main.py && cd ..`\n')
        sys.path.pop(0)
        sys.exit(1)
    with open('./manifest.json') as f:
        manifest = json.load(f)
    with open('./.secret') as f:
        secret = f.read()
    style = manifest['app']['style']
    if style.startswith('https://'):
        pass
    elif style.startswith('/'):
        pass
    else:
        style = importlib.import_module(style)
    app = Frame(
        package=manifest['app']['package'],
        secret=secret,
        permissions=manifest['accounts']['permissions'],
        style=style,
        icon=manifest['app']['icon'],
        default_network=manifest['accounts']['default_network'],
        loginview=manifest['app']['loginview'],
        environment={},
        cors=manifest['app']['cors'],
    )
    app.routes = manifest['app']['routing']
    if 'default_logging.py' in os.listdir('./'):
        default_logging_spec = importlib.util.spec_from_file_location('default_logging', './default_logging.py')
        default_logging = importlib.util.module_from_spec(default_logging_spec)
        default_logging_spec.loader.exec_module(default_logging)
        app.default_logging(default_logging.default_logging)
    if 'environment.py' in os.listdir('./'):
        environment_spec = importlib.util.spec_from_file_location('environment', './environment.py')
        environment = importlib.util.module_from_spec(environment_spec)
        environment_spec.loader.exec_module(environment)
        app.environment = environment.environment
    if 'models.py' in os.listdir('./'):
        models_spec = importlib.util.spec_from_file_location('models', './models.py')
        models = importlib.util.module_from_spec(models_spec)
        models_spec.loader.exec_module(models)
        Database(app, f"sqlite:///{manifest['app']['database_filename']}.db", models.Base)
        app.db.create_all()
    return app, {
        'port': manifest['development']['port'],
        'host': manifest['development']['host'],
        'debug': manifest['development']['debug'],
    }


def run(*args) -> int:
    app, runtime_args = build_frame(*args)
    app.run(host=runtime_args['host'], port=runtime_args['port'], debug=runtime_args['debug'])
    return 0


def cmdline() -> int:
    sys.path.insert(0, './')
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python -m bevyframe <path to project>")
        return 256
    command = args.pop(0)
    if command == "init":
        ret = init(*args)
    elif command == "new":
        ret = new(*args)
    elif command == "run":
        ret = run(*args)
    elif command == "main":
        ret = main(*args)
    else:
        print("Unknown command")
        ret = 1
    sys.path.pop(0)
    return ret
