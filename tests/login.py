from bevyframe import Request, Response, Page, Widget, redirect


def get(request: Request) -> Page:
    return Page(
        title='Login - BevyFrame Test App',
        description='BevyFrame Test App',
        selector='body_blue',
        childs=[
            Widget(
                'form',
                method='POST',
                childs=[
                    Widget(
                        'p',
                        childs=[z]
                    )
                    for z in [
                        Widget(
                            'input',
                            selector='textbox grey',
                            name=y[0],
                            type=y[1],
                            placeholder=y[2],
                            value=y[3]
                        )
                        for y in [
                            ['email', 'text', 'Email Address', ''],
                            ['password', 'password', 'Password', '']
                        ]
                    ] + [
                        Widget(
                            'input',
                            selector='button',
                            type='submit',
                            value='Login'
                        )
                    ]
                ]
            )
        ]
    )


def post(request: Request) -> Response:
    resp = redirect('/')
    resp.login(request.form['email'], request.form['password'])
    return resp
