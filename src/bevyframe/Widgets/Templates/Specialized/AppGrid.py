from bevyframe.Widgets.Style import Size, Overflow, OverflowBehavior, Margin, Padding, Position, Align, Cursor, Color
from bevyframe.Widgets.Templates.Containers import Container, Box
from bevyframe.Widgets.Templates.Media import Image
from bevyframe.Widgets.Templates.Texts import Heading, Label
from bevyframe.Widgets.Templates.Icon import Icon


class AppGridChildItem:
    def __init__(self, name: str, icon: str, url: str, sub_icon: str = ""):
        self.name = name
        self.icon = icon
        self.url = url
        self.sub_icon = sub_icon


class AppGridChild:
    def __init__(self, title: str, items: list[AppGridChildItem]):
        self.title = title
        self.items = items


class AppGrid:
    def __init__(self, children: list[AppGridChild]):
        self.children = children

    def bf_widget(self) -> list[str | dict | list]:
        return Container(
            children=[
                Container([
                    Heading(child.title),
                    Container(
                        width=Size.percent(100),
                        max_width=Size.percent(100),
                        overflow=Overflow(y=OverflowBehavior.scroll),
                        margin=Margin(
                            left=Size.pixel(-15),
                            right=Size.pixel(-15),
                        ),
                        padding=Padding(
                            right=Size.pixel(15),
                            left=Size.pixel(15),
                        ),
                        child=Container(
                            css={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '15px'},
                            width=Size.max_content,
                            children=[
                                Container(
                                    cursor=Cursor.pointer,
                                    onclick=f"window.location.href='{item.url}'",
                                    children=[
                                        Box(
                                            border_radius=Size.percent(40),
                                            width=Size.pixel(100),
                                            height=Size.pixel(100),
                                            padding=Size.pixel(0),
                                            child=Container(
                                                height=Size.pixel(50) if "/" in item.icon else Size.max_content,
                                                width=Size.pixel(50) if "/" in item.icon else Size.max_content,
                                                position=Position.absolute(
                                                    top=Size.percent(50),
                                                    left=Size.percent(50),
                                                ),
                                                padding=Size.pixel(0),
                                                margin=Size.pixel(0),
                                                css={'transform': 'translate(-50%, -50%)'},
                                                child=(
                                                    Image(
                                                        src=item.icon,
                                                        alt=item.name,
                                                        height=Size.percent(100),
                                                        width=Size.percent(100),
                                                        aspect_ratio=1,
                                                    )
                                                    if "/" in item.icon else
                                                    Icon(item.icon, size=60)
                                                )
                                            ),
                                        ),
                                    ] + ([
                                        Box(
                                            border_radius=Size.percent(50),
                                            width=Size.pixel(40),
                                            height=Size.pixel(40),
                                            padding=Size.pixel(0),
                                            margin=Margin(
                                                top=Size.pixel(-45),
                                                left=Size.pixel(60),
                                            ),
                                            background_color=Color.hex("80808080"),
                                            child=Container(
                                                height=Size.pixel(50) if "/" in item.icon else Size.max_content,
                                                width=Size.pixel(50) if "/" in item.icon else Size.max_content,
                                                padding=Size.pixel(5),
                                                margin=Size.pixel(0),
                                                child=Icon(item.sub_icon, size=30)
                                            ),
                                        ),
                                    ] if item.sub_icon else []) + [
                                        Label(
                                            innertext=item.name,
                                            width=Size.percent(100),
                                            text_align=Align.center,
                                        )
                                    ],
                                )
                                for item in child.items
                            ],
                        )
                    )
                ])
                for child in self.children
                if len(child.items) > 0
            ]
        ).bf_widget()
