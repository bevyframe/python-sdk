import os

from bevyframe.Widgets.Style import Size, Align, Overflow
from bevyframe.Widgets.Templates import Container, Box, Label
from bevyframe.Widgets.Widget import Widget


class Tab:
    def __init__(self, name: str, label: str, children: list = None, child=None):
        self.name = name
        self.label = label
        if children:
            self.content = children
        elif child:
            self.content = [child]
        else:
            raise ValueError("Either 'children' or 'child' must be provided for Tab content.")

    def __repr__(self):
        return self.label


class TabView:
    def __init__(self, tabs: list[Tab]):
        if not tabs:
            raise ValueError("At least one tab must be provided.")
        self.tabs = tabs
        self.hash = os.urandom(8).hex()

    def __repr__(self):
        return f"TabView(tabs={self.tabs})"

    def bf_widget(self) -> list[str | dict | list]:
        return Container(
            children=[
                Widget(
                    'div',
                    selector="tab-container",
                    css={"position": "relative"},
                    children=[
                        Widget("style", innertext='\n'.join([
                            f"#tab{i}-{self.hash}:not(:checked) ~ .tab-bar label[for='tab{i}-{self.hash}'] .tab-label {{ background-color: #00000000; border-color: #00000000; }}" +
                            f"#tab{i}-{self.hash}:checked ~ .content #content{i}-{self.hash} {{ display: block !important; }}"
                            for i in range(len(self.tabs))
                        ]))
                    ] + [
                        Widget(
                            "input",
                            type="radio",
                            name=f"tabs-{self.hash}",
                            id=f"tab{i}-{self.hash}",
                            checked=(i == 0),
                            css={"display": "none"}
                        )
                        for i in range(len(self.tabs))
                    ] + [
                        Widget(
                            "div",
                            selector="tab-bar",
                            css={
                                "display": "flex",
                                "position": "relative",
                                "overflow-x": "scroll",
                            },
                            children=[
                                Widget(
                                    "label",
                                    # innertext=,
                                    child=Container(
                                        selector="the_box tab-label",
                                        padding=Size.pixel(10),
                                        text_align=Align.center,
                                        innertext=Label(self.tabs[i].label)
                                    ),
                                    assigned=f"tab{i}-{self.hash}",
                                    selector="tab",
                                    padding=Size.pixel(5),
                                    min_width=Size.pixel(150),
                                    css={
                                        "flex": "1",
                                        "textAlign": "center",
                                        "cursor": "pointer",
                                        "transition": "color 0.3s"
                                    },
                                )
                                for i in range(len(self.tabs))
                            ],
                        ),
                        Widget(
                            "div",
                            selector="content",
                            children=[
                                Widget(
                                    "div",
                                    id=f"content{i}-{self.hash}",
                                    selector="tab-content",
                                    css={
                                        "padding": "20px 10px",
                                        "display": "none",
                                     },
                                    children=self.tabs[i].content
                                )
                                for i in range(len(self.tabs))
                            ]
                        )
                    ]
                )
            ]
        ).bf_widget()
