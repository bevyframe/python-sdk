from bevyframe import Widget
print(Widget('html',lang='en',
    childs=[
        Widget('head',
            childs=[
                Widget('meta', charset='UTF-8'),
                Widget('meta', name='viewport', content='width=device-width, initial-scale=1.0'),
                Widget('link', rel='stylesheet', href='/static/index.css'),
                Widget('title', innertext='Web App'),
            ]
        ),
        Widget('body',
            childs=[
                Widget('h1', innertext=f'Hello, {"username"}!'),
                Widget('p', innertext={'session':'1234567890'})
            ]
        )
    ]
))