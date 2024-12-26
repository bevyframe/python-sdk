from datetime import datetime
from bevyframe.Features.Login import get_session
from bevyframe.Objects.Context import Context


def receiver(self, environ):
    req_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    recv = {
        'method': environ['REQUEST_METHOD'],
        'path': environ['PATH_INFO'],
        'protocol': environ.get('SERVER_PROTOCOL', 'http/1.1'),
        'headers': {},
        'body': environ['wsgi.input'].read().decode() if 'wsgi.input' in environ else '',
        'credentials': None,
        'query': {},
        'ip': environ['REMOTE_ADDR']
    }
    if environ['QUERY_STRING']:
        recv['path'] += f"?{environ['QUERY_STRING']}"
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
    id_on_log = recv['ip'] if recv['credentials']['email'].split('@')[0] == 'Guest' else recv['credentials']['email']
    if recv['path'].startswith('/.well-known/bevyframe/'):
        feature = recv['path'].removeprefix('/.well-known/bevyframe/')
        if feature == 'proxy':
            recv['log'] = f"(   ) {id_on_log} [{req_time}] {r.json['func']}({', '.join([repr(i) for i in r.json['args']])}) -> "
        elif feature == 'pwa.webmanifest':
            recv['log'] = f"(   ) {id_on_log} [{req_time}] GET PWA Manifest"
        else:
            f"(   ) {id_on_log} [{req_time}] Unknown Built-in Feature: {feature}"
    elif self.default_logging_str is None:
        recv['log'] = f"(   ) {id_on_log} [{req_time}] {recv['method']} {recv['path']}"
    else:
        formatted_log = self.default_logging_str(r, req_time)
        if isinstance(formatted_log, tuple):
            formatted_log, display_status_code = formatted_log
        formatted_log = formatted_log.replace('\n', '').replace('\r', '')
        recv['log'] = ('(   ) ' if display_status_code else '      ') + formatted_log
    print(recv['log'], end='', flush=True)
    return recv, req_time, r, display_status_code
