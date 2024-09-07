from bevyframe import *
from TheProtocols import User, Permission
from datetime import datetime, UTC
import hereus_ui_3_2

app = Frame(
    package='dev.islekcaganmert.bevyframe.stdin',
    developer='islekcaganmert@hereus.net',
    administrator=None,
    secret='5d9547e68c469b5e4b97b273e760',  # secrets.token_hex(secrets.randbits(4))
    style=hereus_ui_3_2,
    icon='/favicon.png',
    keywords=['Test'],
    loginview='login.py',
    did='did:plc:demo',
    default_network='localhost',
    permissions=[
        Permission.InterApp
    ]
)
Database(app, 'sqlite:///test.db')


class Test(app.db.Model):
    __tablename__ = 'test'
    id = DataTypes.Column(DataTypes.Integer, primary_key=True)
    email = DataTypes.Column(DataTypes.String)
    ip = DataTypes.Column(DataTypes.String)
    when = DataTypes.Column(DataTypes.Datetime)


# Shared to all scripts
app.environment = {
    'database': {
        'tables': {
            'test': Test
        }
    }
}


@app.default_logging
def log(context: Context, time: str) -> (str, tuple[str, bool]):
    app.db.add(Test(email=context.email, ip=context.ip, when=datetime.now(UTC)))
    app.db.commit()
    u = context.email
    if u.split('@')[0] == 'Guest':
        u = context.ip
    if context.path in ['/favicon.png']:
        last = app.db.query(Test).order_by(Test.id).all()[-1]
        end = f' at {time.split(' ')[0]} on {time.split(' ')[1]}' if last.email != context.email and last.ip != context.ip else ''
        return f'{"".join([' ' for _ in range(len(u))])} and requested {context.path}{end}', False
    else:
        return f'{u} {'sent form to' if context.method == 'POST' else 'loaded'} {context.path} at {time.split(' ')[0]} on {time.split(' ')[1]}'


@app.route('/user/<email>')
def index(context: Context, email) -> Page:
    u = User(email)
    return Page(
        title='',
        description='',
        color=context.user.id.settings.theme_color,
        childs=[
            Title(f"{u.name} {u.surname}")
        ]
    )


if __name__ == '__main__':
    app.db.create_all()
    app.run('0.0.0.0', 3000, debug=True)
