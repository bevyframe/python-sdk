###### *Alpha Preview 0.0.0*
# BevyFrame
Lightweight Python Web Micro Framework

***Downstream Version, Do Not Use in Production***
## Installing
```
$ wget https://github.com/islekcaganmert/bevyframe/releases/download/Preview/BevyFrame-0.0.0-py3-none-any.whl
$ python3 -m pip install ./BevyFrame-0.0.0-py3-none-any.whl
```
## Simple Example

```
from bevyframe import Frame, renderpage, request, redirect

class routes:
    def index():
        usernames = {'1234567890': 'demo'}
        username = usernames[request.cookies['session']]
        return renderpage('index.html', cuser=username)
    def login():
        request.cookies.update({'session':'1234567890'})
        return redirect('/')
    def __error_page__(error):
        return '<h1>Error Code: '+str(error)+'</h1>'

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