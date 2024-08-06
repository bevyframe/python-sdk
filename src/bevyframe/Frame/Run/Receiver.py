import socket
from datetime import datetime

from bevyframe.Features.Login import get_session
from bevyframe.Objects.Request import Request


def receiver(self, server_socket: socket.socket, default_network: str):
    client_socket, client_address = server_socket.accept()
    req_time = datetime.now().strftime('%Y-%M-%d %H:%m:%S')
    raw = client_socket.recv(1024).decode()
    recv = {
        'method': '',
        'path': '',
        'protocol': '',
        'headers': {},
        'body': '',
        'credentials': None,
        'query': {}
    }
    for crl in range(len(raw.split('\r'))):
        for lfl in range(len(raw.split('\r')[crl].split('\n'))):
            line = raw.split('\r')[crl].split('\n')[lfl]
            if crl == lfl == 0:
                recv['method'], recv['path'], recv['protocol'] = line.split(' ')
            else:
                if ': ' in line:
                    recv['headers'].update({line.split(': ')[0]: line.split(': ')[1]})
                else:
                    recv['body'] += (line + '\r\n')
    recv['path'] = '/'.join([('' if i == '..' else i) for i in recv['path'].split('/')])
    try:
        recv['credentials'] = get_session(
            self.secret,
            recv['headers']['Cookie'].split('s=')[1].split(';')[0]
        ) if 's=' in recv['headers']['Cookie'] else None
        if recv['credentials'] is None:
            recv['credentials'] = {
                'email': f"Guest@{default_network}",
                'password': ''
            }
    except KeyError:
        pass
    if recv['credentials'] is None:
        recv['credentials'] = {
            'email': 'Guest@hereus.net',
            'password': ''
        }

    if self.default_logging_str is None:
        r = None
        if recv['credentials']['email'].split('@')[0] == 'Guest':
            print(f"(   ) {client_address[0]} [{req_time}]", end=' ')
        else:
            print(f"\r(   ) {recv['credentials']['email']} [{req_time}]",
                  end=' ')
        print(f"{recv['method']} {recv['path']} {recv['protocol']}", end='', flush=True)
    else:
        r = Request(recv, self)
        print('(   ) ' + self.default_logging_str(r, req_time).replace('\n', '').replace('\r', ''), end='', flush=True)
    recv['path'] = recv['path'].split('?')[0]
    return recv, client_socket, req_time, r
