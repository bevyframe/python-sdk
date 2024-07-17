from bevyframe.Widgets.Widget import Widget

Navbar = lambda childs: Widget(
    'nav',
    selector='Navbar',
    id='navbar',
    childs=childs
)

NavIcon = lambda src: Widget(
    'a',
    selector='titleicon',
    childs=[
        Widget(
            'img',
            src=src,
            height='36px',
            style={'padding-bottom': '10px'}
        )
    ]
)

NavItem = lambda icon, link, alt, active = False: Widget(
    'a',
    selector=('active' if active else 'inactive'),
    href=link,
    childs=[
        Widget('button', childs=[
            Widget(
                'span',
                selector=f'material-symbols-rounded',
                innertext=icon,
                alt=alt
            )
        ])
    ]
)
