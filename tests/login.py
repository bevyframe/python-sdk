from bevyframe import *
from TheProtocols import ID, CredentialsDidntWorked


def log(r: Request, time: str) -> str:
    if r.method == 'POST':
        return f'{r.form['email']} is trying to login at {time.split(' ')[0]} on {time.split(' ')[1]}'
    else:
        return None


def get(request: Request) -> Page:
    return Page(
        title='Login - BevyFrame Test App',
        description='BevyFrame Test App',
        color=Theme.blue,
        childs=[
            Form(
                'POST',
                childs=[
                    Line([z])
                    for z in [
                        Textbox(y[0], selector='grey', type=y[1], placeholder=y[2])
                        for y in [
                            ['email', 'text', 'Email Address'],
                            ['password', 'password', 'Password']
                        ]
                    ] + [Button(innertext='Login')]
                ]
            )
        ]
    )


def post(request: Request) -> Response:
    resp = redirect('/')
    try:
        ID(request.form['email'], request.form['password'])
        resp.login(request.form['email'], request.form['password'])
        print(', success', end='', flush=True)
    except CredentialsDidntWorked:
        print(', failed', end='', flush=True)
    return resp
