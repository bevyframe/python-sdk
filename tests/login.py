from bevyframe import *


def log(r: Context, time: str) -> (str, None):
    if r.method == 'POST':
        return f'{r.form['email']} is trying to login at {time.split(' ')[0]} on {time.split(' ')[1]}'
    else:
        return None


def get(context: Context) -> Page:
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
                        Textbox(y[0], selector='grey', type=y[1], placeholder=y[2], value=context.headers['Cookie'])
                        for y in [
                            ['email', 'text', 'Email Address'],
                            ['password', 'password', 'Password']
                        ]
                    ] + [Button(innertext='Login')]
                ]
            )
        ]
    )


def post(context: Context) -> (Response, Page):
    resp = context.redirect('/')
    if resp.login(context.form['email'], context.form['password']):
        print(', success', end='', flush=True)
        return resp
    else:
        print(', failed', end='', flush=True)
        return get(context)
