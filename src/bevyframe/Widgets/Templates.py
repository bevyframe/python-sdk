from bevyframe.Widgets.Widget import Widget


Title = lambda innertext, **kwargs: Widget('h1', innertext=innertext, **kwargs)
Box = lambda **kwargs: Widget('div', selector='the_box', **kwargs)
Post = lambda **kwargs: Widget('div', selector='post', **kwargs)
Line = lambda childs, **kwargs: Widget('p', childs=childs if isinstance(childs, list) else [childs], **kwargs)
Label = lambda innertext, **kwargs: Line(childs=innertext, **kwargs)
Textbox = lambda name, selector = '', **kwargs: Widget('input', name=name, id=name, selector=f'textbox {selector}', **kwargs)
Button = lambda selector = '', **kwargs: Widget('button', selector=f'button {selector}', **kwargs)
Form = lambda method, childs: Widget('form', method=method, childs=childs)
Bold = lambda innertext: Widget('b', innertext=innertext)
Italic = lambda innertext: Widget('i', innertext=innertext)
Link = lambda innertext, url, external=False: Widget('a', innertext=innertext, href=url, selector='link', **({'target': '_blank'} if external else {}))
