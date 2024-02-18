from bevyframe import Frame, Page, Widget, protocol, Request, Response
import requests

app = Frame(
    package='dev.islekcaganmert.bevyframe.stdin',
    developer='islekcaganmert@hereus.net',
    administrator='islekcaganmert@hereus.net',
    secret='5d9547e68c469b5e4b97b273e760',  # secrets.token_hex(secrets.randbits(4))
    style=requests.get('https://git.hereus.net/HereUS/HereUS-UI-3.1/raw/master/HereUS-UI-3.1.json').json(),
    icon='/favicon.png',
    keywords=['Test']
)


@app.route('/user/<email>')
def index(request: Request, email) -> Page:
    u = protocol.find_user(email)
    return Page(
        title='',
        description='',
        selector='body_blue',
        childs=[
            Widget('h1', innertext=f"{u['name']} {u['surname']}")
        ]
    )


app.run('0.0.0.0', 80, False)