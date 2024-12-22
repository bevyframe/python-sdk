from bevyframe import *

blacklist = lambda: ["demo@hereus.net"]


@login_required
def get(context: Context) -> (Page, Response):
    '''last_ip_query = context.app.db.query(context.env['database']['tables']['test']).filter_by(email=context.email).all()
    if len(last_ip_query) == 0:
        raise Error404
    last_ip = last_ip_query[-1].ip'''
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        color=context.user.id.settings.theme_color,
        childs=[
            Title(f'Hello, {context.user.id.name} {context.user.id.surname} from {context.user.network}!'),
            Box(
                width=Size.max_content,
                text_align=Align.center,
                childs=[
                    # Line([Textbox('', type="text", placeholder='textbox', value=last_ip)]),
                    Line([Button(innertext='Button')]),
                    Line([Button(selector='small', innertext='Button')]),
                    Line([Button(selector='mini', innertext='Button')])
                ]
            )
        ]
    )
