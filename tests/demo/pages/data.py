from bevyframe import *


def post(context: Context) -> Response:
    context.data['value'] = context.form['entry']
    return context.start_redirect("/data.html")
