from bevyframe import *
from TheProtocols import User
import hereus_ui_3_2

app = Frame(
    package='dev.islekcaganmert.bevyframe.stdin',
    developer='islekcaganmert@hereus.net',
    administrator=None,
    secret='5d9547e68c469b5e4b97b273e760',  # secrets.token_hex(secrets.randbits(4))
    style=hereus_ui_3_2,
    icon='/favicon.png',
    keywords=['Test']
)


@app.default_logging
def log(r: Request, time: str) -> str:
    u = r.email
    if u.split('@')[0] == 'Guest':
        u = r.ip
    return f'{u} {'sent form to' if r.method == 'POST' else 'landed on'} {r.path} at {time.split(' ')[0]} on {time.split(' ')[1]}'


@app.route('/user/<email>')
def index(request: Request, email) -> Page:
    u = User(email)
    return Page(
        title='',
        description='',
        color=request.user.id.settings.theme_color,
        childs=[
            Title(f"{u.name} {u.surname}")
        ]
    )


if __name__ == '__main__':
    app.run('0.0.0.0', 80, True)
