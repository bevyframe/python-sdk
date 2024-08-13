from bevyframe import *


def post(r: Request) -> Page:
    r.data['value'] = r.form['entry']
    return get(r)


def get(r: Request) -> Page:
    if 'value' not in r.data.keys():
        r.data = {'value': 'Hello, World!'}
    return r.render_template('data.html', value=r.data['value'])
