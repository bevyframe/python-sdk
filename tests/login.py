from bevyframe import *


def get(request: Request) -> Page:
    return Page(
        title='Login - BevyFrame Test App',
        description='BevyFrame Test App',
        selector='body_blue',
        childs=[
            Form(
                'POST',
                childs=[
                    Line(z)
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
    resp.login(request.form['email'], request.form['password'])
    return resp
