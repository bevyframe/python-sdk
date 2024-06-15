from bevyframe import *


def get(r: Request) -> Page:
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        selector='body_blue',
        childs=[
            Title('404 Not Found')
        ]
    )
