from bevyframe.Widgets.Templates.Containers import Line
from bevyframe.Widgets.Widget import Widget

Label = lambda innertext, no_newline = False, **kwargs: Widget(
    'a',
    childs=[innertext],
    **kwargs
) if no_newline else Line(
    childs=[innertext],
    **kwargs
)

Bold = lambda innertext: Widget(
    'b',
    innertext=innertext
)

Italic = lambda innertext: Widget(
    'i',
    innertext=innertext
)

Link = lambda innertext, url, external=False, **kwargs: Widget(
    'a',
    innertext=innertext,
    href=url,
    selector='link',
    **({'target': '_blank'} if external else {}),
    **kwargs
)

Title = lambda childs, **kwargs: Widget(
    'h1',
    childs=childs if isinstance(childs, list) else [childs],
    **kwargs
)

SubTitle = lambda childs, **kwargs: Widget(
    'h2',
    childs=childs if isinstance(childs, list) else [childs],
    **kwargs
)

Heading = lambda childs, **kwargs: Widget(
    'h3',
    childs=childs if isinstance(childs, list) else [childs],
    **kwargs
)
