from bevyframe import *

blacklist = lambda: ["demo@hereus.net"]


@login_required
def get(request: Request) -> (Page, Response):
    last_ip = request.app.db.query(request.env['database']['tables']['test']).filter_by(email=request.email).first().ip
    return Page(
        title='BevyFrame Test App',
        description='BevyFrame Test App',
        color=request.user.id.settings.theme_color,
        childs=[
            Title(f'Hello, {request.user.id.name} {request.user.id.surname} from {request.user.network}!'),
            Box(
                width=Size.max_content,
                text_align=Align.center,
                childs=[
                    Line([Textbox('', type="text", placeholder='textbox', value=last_ip)]),
                    Line([Button(innertext='Button')]),
                    Line([Button(selector='small', innertext='Button')]),
                    Line([Button(selector='mini', innertext='Button')])
                ]
            )
        ]
    )
