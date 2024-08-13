from bevyframe import *


def post(r: Request) -> Page:
    r.data['value'] = r.form['entry']
    return get(r)


def get(r: Request) -> Page:
    if 'value' not in r.data.keys():
        r.data = {'value': 'Hello, World!'}
    return Page(
        title='Data',
        color=r.user.id.settings.theme_color,
        childs=[
            Form(
                method='POST',
                childs=[
                    Textbox('entry', value=r.data.get('value')),
                ]
            )
        ]
    )
