import sys
from bevyframe.Objects.Context import Context


def run() -> int:
    req_headers = {}
    req_body = b''

    in_headers = True
    for line in sys.stdin.buffer.readlines():
        if in_headers:
            if line.strip() == b'':
                in_headers = False
            else:
                parts = line.decode().split(':', 1)
                req_headers.update({parts[0]: str(parts[1]).removesuffix('\n').removeprefix(' ')})
        else:
            req_body += line
    http_headers = {}

    for i in req_headers:
        if i.startswith('Header.'):
            http_headers.update({i.removeprefix('Header.'): req_headers[i]})

    r = Context({
        'method': req_headers.get('Method', 'GET'),
        'path': req_headers.get('Path', '/'),
        'protocol': 'bevyframe',
        'headers': http_headers,
        'body': req_body,
        'credentials': {
            'email': req_headers['Cred.Email'],
            'token': req_headers['Cred.Token']
        },
        'query': '',
        'ip': req_headers.get('IP', '127.0.0.1'),
        'permissions': req_headers.get('Permissions', '').split(','),
        'package': req_headers.get('Package'),
        'loginview': req_headers.get('LoginView'),
    })

    login_req = sys.argv[2] == 'loginRequired' if len(sys.argv) > 2 else False
    resp = r.render_template(sys.argv[1], login_req=login_req)

    out = b"BevyFrame 200\n"
    out += b"Content-Type: text/html\n\n"
    out += str(resp).encode() + b'\n'
    out += b'\n'
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    return 0
