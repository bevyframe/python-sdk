from bevyframe.Widgets.Style import substract_style, Size, Position, Margin, OverflowBehavior, Overflow, Padding
from bevyframe.Widgets.Templates import Container, Box


class DualContainer:
    def __init__(self, left_children: list, right_children: list) -> None:
        self.left_children = left_children
        self.right_children = right_children

    def bf_widget(self) -> list[str | dict | list]:
        return Container(
            children=[
                Container(
                    selector=f'dual-container dual-container-left',
                    style={
                        'overflow-y': 'auto',
                        'transition': 'all 0.3s ease',
                        'height': '100%',
                    },
                    child=Box(
                        children=self.left_children,
                        width=substract_style(Size.percent(100), Size.pixel(45)),
                        padding=Size.pixel(15),
                        max_height=Size.percent(100),
                        overflow=Overflow(y=OverflowBehavior.scroll),
                        position=Position.relative(
                            top=Size.pixel(5),
                            left=Size.pixel(5),
                            right=Size.pixel(5),
                            bottom=Size.pixel(5),
                        ),
                    ),
                ),
                Container(
                    selector=f'dual-container dual-container-right',
                    css={
                        'overflow-y': 'auto',
                        'transition': 'all 0.3s ease',
                        'height': '100%',
                    },
                    padding=Padding(
                        left=Size.pixel(10),
                        right=Size.pixel(10),
                    ),
                    children=self.right_children,
                ),
            ]
        ).bf_widget()