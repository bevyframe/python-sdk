from bevyframe.Frame import Frame
import json
import os
import sys
import importlib.util


def init(*_) -> int:
    if os.system("which pymake > /dev/null 2>&1") != 0:
        print("ERROR: pymake is not installed")
        input("Please create your standard Python environment, then click any key to continue...")
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
    generate_secret()
    os.mkdir('assets')
    os.mkdir('strings')
    os.mkdir('functions')
    with open('models.py', 'w') as f:
        f.write('from bevyframe import *\n\nclass Base(DeclarativeBase):\n\tpass\n\n')
    with open('README.md') as f:
        project_name = f.read().splitlines()[0].removeprefix('# ')
    manifest = {
        "@context": "https://bevyframe.islekcaganmert.me/ns/manifest",
        "app": {
            "name": project_name,
            "short_name": project_name,
            "orientation": "any",
            "version": "1.0.0",
            "package": input("Package: "),
            "style": input("\nStyle name or CSS URL/path: "),
            "icon": "/assets/favicon.png",
            "loginview": "/login.py",
            "shareview": "/share.py",
            "offlineview": "/offline.py",
            "accept_media": [],
            "database_filename": "app",
            "allow_multiple_instance": True,
            "shortcuts": {},
            "cors": False,
            "routing": {},
            "disable_features": []
        },
        "publishing": {
            "description": input('\nDescription: '),
            "screenshots": []
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
            "android": {
            "api_level": [33, 35],
                "permissions": [],
                "features": [],
                "adaptive_icon": {
                    "foreground": "",
                    "background": ""
                }
            },
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
    os.system("bevyframe new /login.py 'Login - " + project_name.replace('\'', '\\\'') + "'")
    os.system("bevyframe new /share.py '" + project_name.replace('\'', '\\\'') + "'")
    os.system("bevyframe new /offline.py '" + project_name.replace('\'', '\\\'') + "'")
    print()
    return 0


def new(*args) -> int:
    with open(f'./pages/{args[0].removeprefix("/").removesuffix("/")}' + ('' if args[0].endswith('.py') else '/__init__.py'), 'w') as f:
        f.write(f'''
from bevyframe import *


def get(context: Context) -> Page:
    return Page(
        title="{input("Title: ") if len(sys.argv) < 3 else args[1]}",
        color=context.user.id.settings.theme_color,
        childs=[
            # Place Navbar above Root,
            Root([
                # Place your content here
            ])
        ]
    )
            '''.removeprefix('\n'))
    return 0


def build_frame(*_) -> tuple[Frame, dict]:
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
        disable_features=manifest['app']['disable_features']
    )
    if "DynamicRouting" not in app.disabled:
        app.routes = manifest['app']['routing']
    if 'default_logging.py' in os.listdir('./') and 'CustomLogging' not in app.disabled:
        default_logging_spec = importlib.util.spec_from_file_location('default_logging', './default_logging.py')
        default_logging = importlib.util.module_from_spec(default_logging_spec)
        default_logging_spec.loader.exec_module(default_logging)
        app.default_logging(default_logging.default_logging)
    if 'Environment' not in app.disabled and 'environment.py' in os.listdir('./'):
        environment_spec = importlib.util.spec_from_file_location('environment', './environment.py')
        environment = importlib.util.module_from_spec(environment_spec)
        environment_spec.loader.exec_module(environment)
        app.environment = environment.environment
    if 'Database' not in app.disabled and 'models.py' in os.listdir('./'):
        from bevyframe.Features.Database import Database
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
    if len(args) == 0:
        print("Platform not provided. web/ios/android/nt/macos/snap/flatpak/luos")
        return 1
    if args[0] == 'web':
        app, runtime_args = build_frame(*args)
        app.run(host=runtime_args['host'], port=runtime_args['port'], debug=runtime_args['debug'])
        return 0
    elif args[0] in ['nt', 'macos', 'snap', 'flatpak']:
        try:
            from bevyframe.Platforms.Desktop import Desktop
            return Desktop().start()
        except ModuleNotFoundError:
            print(f"SDK for {args[0]} is not installed.\n")
            return 1


def dispatcher(*_) -> int:
    with open('./dispatcher.json', 'w') as f:
        f.write(json.dumps({
            "@context": "https://bevyframe.islekcaganmert.me/ns/dispatcher",
            "domains": {}
        }))
    return 0


def count(filename: str) -> int:
    if '__pycache__' in filename:
        return 0
    if os.path.exists(filename):
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                return len(f.readlines())
        total = 0
        for i in os.listdir(f'{filename}/'):
            total += count(f'{filename}/{i}')
        return total
    return 0


def countlines() -> int:
    total = 0
    for i in ['functions', 'pages', 'src', 'widgets', 'default_logging.py', 'environment.py', 'models.py']:
        total += count(i)
    print(f"\nTotal {total}\n")
    return 0


def generate_secret() -> int:
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives.hashes import SHA256
    from cryptography.hazmat.backends import default_backend
    import os
    salt = os.urandom(16)
    print('\nGenerating secret.')
    raw_key = input('Enter random characters, then click enter: ').encode()
    key = HKDF(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        info=b'bevyframe-sessions',
        backend=default_backend()
    ).derive(raw_key)
    print()
    with open('.secret', 'w') as f:
        f.write(key.hex())
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
        from bevyframe.Helpers.MainPyCompiler import MainPyCompiler
        ret = MainPyCompiler(*args)
    elif command == "dispatcher":
        ret = dispatcher(*args)
    elif command == "count":
        ret = countlines()
    elif command == "secret":
        ret = generate_secret()
    else:
        print("Unknown command")
        ret = 1
    sys.path.pop(0)
    return ret
