from bevyframe import Page, Widget, Request, get_admin, redirect, Response, current_user
import json


def get(request: Request) -> (Page, Response):
    if request.email.split('@')[0] == 'Guest':
        return redirect('/login.py')
    cuser = current_user(request)
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        selector='body_blue',
        childs=[
            Widget('h1', innertext=f'Hello, {cuser.name} {cuser.surname}!'),
            Widget('div', selector='the_box', style={
                "width": "max-content",
                "text-align": "center"
            }, childs=[
                Widget('p', childs=[
                    Widget('input', type="text", selector='textbox', placeholder='textbox')
                ]),
                Widget('p', childs=[
                    Widget('button', selector='button', innertext='Button')
                ]),
                Widget('p', childs=[
                    Widget('button', selector='button small', innertext='Button')
                ]),
                Widget('p', childs=[
                    Widget('button', selector='button mini', innertext='Button')
                ])
            ])
        ]
    )