from bevyframe import *


def change_environment(context: Context, text: str) -> change_html:
    context.env['text'] = text
    return change_html('h1#title', safe(text))
