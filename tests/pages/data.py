from bevyframe import *


def post(context: Context) -> str:
    context.data['value'] = context.form['entry']
    return get(context)


def get(context: Context) -> str:
    if 'value' not in context.data.keys():
        context.data = {'value': 'Hello, World!'}
    return context.render_template('data.html', value=context.data['value'])
