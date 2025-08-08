from bevyframe.Widgets.Style import substract_style, Size, Cursor, Margin
from bevyframe.Widgets.Templates import Box, Container, Icon, Heading, Label


class Notification:
    def __init__(self, onclick: str, title: str, description: str, url: str, type: str, can_delete: bool) -> None:
        self.can_delete = can_delete
        self.onclick = onclick
        self.title = title
        self.description = description
        self.url = url
        self.type = type  # 'info', 'warning', 'error'

    def bf_widget(self) -> list[str | dict | list]:
        return Box(
            selector=f'{self.type}-notification',
            width=substract_style(Size.percent(100), Size.pixel(5)),
            cursor=Cursor.pointer,
            margin=Margin(
                top=Size.pixel(15),
            ),
            padding=Size.pixel(0),
            css={'display': 'flex'},
            children=[
                Container(
                    onclick="window.location.href='" + self.url.replace('\'', '\\\'') + "'",
                    width=substract_style(Size.percent(100), Size.pixel(80)),
                    css={'display': 'flex'},
                    children=[
                        Container(
                            height=Size.percent(100),
                            width=Size.pixel(80),
                            child=Container(
                                margin=Margin(
                                    top=Size.pixel(20),
                                    left=Size.pixel(20),
                                ),
                                child=Icon(
                                    self.type,
                                    size=40,
                                    margin=Margin(
                                        right=Size.pixel(10),
                                    ),
                                ),
                            ),
                        ),
                        Container(
                            children=[
                                Heading(
                                    self.title,
                                    margin=Margin(
                                        bottom=Size.pixel(5),
                                    ),
                                ),
                                Label(
                                    self.description,
                                    margin=Margin(
                                        top=Size.pixel(0),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                Container(
                    height=Size.percent(100),
                    width=Size.pixel(80),
                    onclick=self.onclick,
                    child=Container(
                        margin=Margin(
                            top=Size.pixel(20),
                            left=Size.pixel(20),
                        ),
                        child=Icon(
                            "close",
                            size=40,
                            margin=Margin(
                                right=Size.pixel(10),
                            ),
                        ),
                    ),
                )
                if self.can_delete else Container(children=[]),
            ],
        ).bf_widget()