from bevyframe import *
from TheProtocols import *


def activity(context: Context) -> Activity:
    u = User(context.query['email'])
    return Activity(
        name=f"{u.name} {u.surname}",
        prop2="demo"
    )


def get(context: Context) -> Page:
    u = User(context.query['email'])
    return Page(
        title='',
        description='',
        color=context.user.id.settings.theme_color,
        childs=[
            Title(f"{u.name} {u.surname}")
        ]
    )
