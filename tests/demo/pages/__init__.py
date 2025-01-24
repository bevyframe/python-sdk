from bevyframe import *
from models import Test
from widgets.CustomButton import CustomButton

blacklist = lambda: ["demo@hereus.net"]


@login_required
def get(context: Context) -> (Page, Response):
    last_ip_query = context.db.query(Test).filter_by(email=context.email).all()
    if len(last_ip_query) == 0:
        raise Error404
    last_ip = last_ip_query[-1].ip
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        color=context.user.id.settings.theme_color,
        childs=[
            Navbar([
                NavItem('home', '/', 'Home', True),
                NavItem('apps', '/env.html', 'Demo'),
            ]),
            Root([
                Title(f'Hello, {context.user.id.name} {context.user.id.surname} from {context.user.network}!'),
                Label(f"You are using {context.browser.device}"),
                Label(f"You are using {context.browser.name} {context.browser.version} which uses WebKit {context.browser.webkit_version}"),
                Label(f"Your browser's language is set to {context.browser.language}"),
                Label(f"Your device has {context.browser.ram} GB of RAM"),
                Label(f"Your bandwith is {context.browser.bandwidth} Mbps"),
                Label(f"Your network type is {context.browser.network_profile}"),
                Label(f"Your last visited profile is {context.last_visited_profile}"),
                Box(
                    width=Size.max_content,
                    text_align=Align.center,
                    childs=[
                        Line([Textbox('', type="text", placeholder='textbox', value=last_ip)]),
                        Line([CustomButton(innertext='Button')]),
                        Line([Button(selector='small', innertext='Button')]),
                        Line([Button(selector='mini', innertext='Button')])
                    ]
                )
            ], margin=Margin(left=Size.pixel(100)))
        ]
    )
