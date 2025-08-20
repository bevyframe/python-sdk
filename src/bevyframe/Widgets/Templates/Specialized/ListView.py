from bevyframe.Widgets.Style import Margin, Size, substract_style, Cursor, BorderRadius
from bevyframe.Widgets.Templates import Container, SubTitle, Heading, Label, Box, Icon, Image


class ListView:
    def __init__(self, sections: list[dict[str, str | list[dict]]]) -> None:
        self.sections = sections

    def bf_widget(self) -> list[str | dict | list]:
        return Container([
            Container([
                SubTitle(section['title'], margin=Margin(bottom=Size.pixel(10))),
                Container([
                    Box(
                        css={'display': 'flex'},
                        height=Size.max_content,
                        padding=Size.pixel(15),
                        width=substract_style(Size.percent(100), Size.pixel(35)),
                        margin=Margin(bottom=Size.pixel(5)),
                        cursor=Cursor.pointer,
                        onclick=section['items'][i]['onclick'],
                        border_radius=(
                            None if len(section['items']) == 1 else
                            BorderRadius(
                                bottom_left=Size.pixel(5),
                                bottom_right=Size.pixel(5),
                            )
                            if i == 0 else
                            BorderRadius(
                                top_left=Size.pixel(5),
                                top_right=Size.pixel(5),
                            )
                            if i == len(section['items']) - 1 else
                            Size.pixel(5)
                        ),
                        children=[
                            Container(
                                margin=Margin(
                                    right=Size.pixel(20),
                                    left=Size.pixel(10),
                                ),
                                child=((
                                    Icon(
                                        section['items'][i]['icon'].icon_name,
                                        size=50,
                                        margin=Margin(right=Size.pixel(0))
                                    )
                                    if isinstance(section['items'][i]['icon'], Icon) else
                                    Image(
                                        src=section['items'][i]['icon'].src,
                                        alt=section['items'][i]['icon'].alt,
                                        width=Size.pixel(50),
                                        height=Size.pixel(50),
                                        **section['items'][i]['icon'].kwargs,
                                    )
                                ) if section['items'][i]['icon'] else Label(""))
                            ),
                            Container([
                                Heading(section['items'][i]['title'], margin=Size.pixel(2)),
                                Label(section['items'][i]['description'], margin=Size.pixel(2))
                            ])
                        ]
                    ) for i in range(len(section['items']))
                ])
            ])
            for section in self.sections
        ]).bf_widget()
