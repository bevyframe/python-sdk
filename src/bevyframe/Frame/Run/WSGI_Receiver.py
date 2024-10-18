from datetime import datetime
from bevyframe.Features.Login import get_session
from bevyframe.Objects.Context import Context


def wsgi_receiver(self, environ):
    req_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    recv = {
        'method': environ['REQUEST_METHOD'],
        'path': environ['PATH_INFO'] + '?' + environ['QUERY_STRING'],
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
    except KeyError:
        pass
    if recv['credentials'] is None:
        recv['credentials'] = {
            'email': f'Guest@{self.default_network}',
            'token': ''
        }
    r = Context(recv, self)
    display_status_code = True
    if self.default_logging_str is None:
        if recv['credentials']['email'].split('@')[0] == 'Guest':
            recv['log'] = f"(   ) {recv['ip']} [{req_time}] {recv['method']} {recv['path']}"
        else:
            recv['log'] = f"\r(   ) {recv['credentials']['email']} [{req_time}] {recv['method']} {recv['path']}"
    else:
        formatted_log = self.default_logging_str(r, req_time)
        if isinstance(formatted_log, tuple):
            display_status_code = formatted_log[1]
            formatted_log = formatted_log[0]
        formatted_log = formatted_log.replace('\n', '').replace('\r', '')
        recv['log'] = ('(   ) ' if display_status_code else '      ') + formatted_log
    print(recv['log'], end='', flush=True)
    return recv, req_time, r, display_status_code
