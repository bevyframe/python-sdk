from bevyframe import *


def log(r: Context, time: str) -> (str, None):
    if r.method == 'POST':
        return f"{r.form['email']} is trying to login at {time.split(' ')[0]} on {time.split(' ')[1]}"
    else:
        return None


def post(context: Context) -> (Response, Page):
    resp = context.start_redirect('/')
    if resp.login(context.form['email'], context.form['password']):
        print(', success', end='', flush=True)
        return resp
    else:
        print(', failed', end='', flush=True)
        return get(context)


def get(context: Context) -> Page:
    return Page(
        title='Login - BevyFrame Test App',
        description='BevyFrame Test App',
        color=Theme.blue,
        childs=[
            Root([
                Box(
                    width=Size.max_content,
                    margin=Margin(
                        top=Size.Viewport.height(10),
                        left=Size.auto,
                        right=Size.auto,
                    ),
                    childs=[
                        Title('Login'),
                        Form(
                            'POST',
                            childs=[
                                Line([z])
                                for z in [
                                    Textbox(y[0], type=y[1], placeholder=y[2])
                                    for y in [
                                        ['email', 'text', 'Email Address'],
                                        ['password', 'password', 'Password']
                                    ]
                                ] + [Button(innertext='Login')]
                            ]
                        )
                    ]
                )
            ])
        ]
    )
