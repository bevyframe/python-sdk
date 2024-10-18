import socket
from datetime import datetime
from bevyframe.Features.Login import get_session
from bevyframe.Objects.Context import Context


def receiver(self, server_socket: socket.socket):
    client_socket, client_address = server_socket.accept()
    req_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request = client_socket.recv(4096).decode()
    body = b""
    if 'connection: keep-alive' in request.lower():
        content_length = None
        for header in request.split("\r\n"):
            if header.startswith("Content-Length:"):
                content_length = int(header.split(":")[1].strip())
                break
        if content_length:
            client_socket.sendall(b'HTTP/1.1 100 Continue\r\n\r\n')
            while len(body) < content_length:
                body += client_socket.recv(4096)
    raw = (request.encode() + b'\r\n' + body).decode()
    recv: dict = {
        'method': '',
        'path': '',
        'protocol': '',
        'headers': {},
        'body': '',
        'credentials': None,
        'query': {},
        'ip': client_address[0]
    }
    raw = raw.replace('\r\n', '\n').replace('\n\r', '\n').replace('\r', '\n')
    raw = raw.replace('\n\n', '\n')
    found_body = False
    for crl in range(len(raw.split('\n'))):
        line = raw.split('\n')[crl]
        if crl == 0:
            s = line.split(' ')
            recv['method'], recv['protocol'] = s[0], s[-1]
            recv['path'] = line.removeprefix(f"{s[0]} ").removesuffix(f" {s[-1]}")
        elif found_body:
            recv['body'] += (line + '\r\n')
        else:
            if line == '':
                found_body = True
            elif ': ' in line:
                recv['headers'].update({
                    line.split(': ')[0]: line.removeprefix(f"{line.split(': ')[0]}: ")
                })
    recv['path'] = '/'.join([('' if i == '..' else i) for i in recv['path'].split('/')])
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
            recv['log'] = f"(   ) {client_address[0]} [{req_time}] {recv['method']} {recv['path']}"
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
    return recv, client_socket, req_time, r, display_status_code
