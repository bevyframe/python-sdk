###### *Alpha Preview 0.1.0*
# BevyFrame
Lightweight Python Web Micro Framework

***Upstream Version, Do Not Use in Production***
## Installing
```bash
$ wget https://github.com/islekcaganmert/bevyframe/releases/download/Preview/BevyFrame-0.1.0-py3-none-any.whl
$ python3 -m pip install ./BevyFrame-0.1.0-py3-none-any.whl
```
## Simple Example

```python
from bevyframe import Frame, renderpage, request, redirect, Widget

class routes:
    def index():
        usernames = {'1234567890': 'demo'}
        username = usernames[request.cookies['session']]
        return Widget('html',
            lang='en',
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
                        Widget('h1', innertext=f'Hello, {username}!'),
                        Widget('p', innertext=request.cookies)
                    ]
                )
            ]
        )
        #return renderpage('index.html', cuser=username, cookies=request.cookies)
    def login():
        request.cookies['session'] = '1234567890'
        return redirect('/')
    def __error_page__(error):
        return Widget('h1',
            childs=[
                f'Error Code: {error}'
            ]
        )

if __name__ == '__main__':
    paths = {'/': [routes.index, {}], '/login': [routes.login, {}]}
    Frame(routes, paths).start_server(host='0.0.0.0', port=8000)
```
## Links
- Documentation: *Soon*
- PyPI Releases: *Soon*
- Source Code: https://github.com/islekcaganmert/bevyframe/
- Issue Tracker: https://github.com/islekcaganmert/bevyframe/issues/
- Community: https://hereus.pythonanywhere.com/communities/BevyFrame
