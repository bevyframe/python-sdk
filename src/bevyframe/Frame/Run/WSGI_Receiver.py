from datetime import datetime
from bevyframe.Features.Login import get_session
from bevyframe.Objects.Context import Context


def wsgi_receiver(self, environ):
    req_time = datetime.now().strftime('%Y-%M-%d %H:%m:%S')
    recv = {
        'method': environ['REQUEST_METHOD'],
        'path': environ['PATH_INFO'],
        'protocol': environ['SERVER_PROTOCOL'],
        'headers': {},
        'body': environ['wsgi.input'].read().decode(),
        'credentials': None,
        'query': {},
        'ip': environ['REMOTE_ADDR']
    }
    for header in environ:
        if header.startswith('HTTP_'):
            key = header[5:].removeprefix('HTTP_').replace('_', '-').title()
            recv['headers'].update({key: environ[header]})
    try:
        recv['credentials'] = get_session(
            self.secret,
            recv['headers']['Cookie'].split('s=')[1].split(';')[0]
        ) if 's=' in recv['headers']['Cookie'] else None
        if recv['credentials'] is None:
            recv['credentials'] = {
                'email': f"Guest@{self.default_network}",
                'password': ''
            }
    except KeyError:
        pass
    if recv['credentials'] is None:
        recv['credentials'] = {
            'email': f'Guest@{self.default_network}',
            'password': ''
        }

    r = Context(recv, self)
    if self.default_logging_str is None:
        if recv['credentials']['email'].split('@')[0] == 'Guest':
            print(f"(   ) {recv['ip']} [{req_time}]", end=' ')
        else:
            print(f"\r(   ) {recv['credentials']['email']} [{req_time}]",
                  end=' ')
        print(f"{recv['method']} {recv['path']} {recv['protocol']}", end='', flush=True)
    else:
        print('WSGI: ' + self.default_logging_str(r, req_time).replace('\n', '').replace('\r', ''), end='', flush=True)

    return recv, req_time, r
