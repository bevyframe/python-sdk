from bevyframe import *


def get(r: Request) -> Page:
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        color=Theme.blue,
        childs=[
            Title('404 Not Found')
        ]
    )
