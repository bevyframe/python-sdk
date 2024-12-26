from bevyframe import *


def get(_: Context) -> Page:
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        color=Theme.blue,
        childs=[
            Title('You are offline')
        ]
    )
