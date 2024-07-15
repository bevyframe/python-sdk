import socket
from datetime import datetime

from bevyframe.Features.Login import get_session
from bevyframe.Objects.Request import Request


def receiver(self, server_socket: socket.socket):
    client_socket, client_address = server_socket.accept()
    print(f"(   ) {client_address[0]} [{datetime.now().strftime('%Y-%M-%d %H:%m:%S')}]", end=' ')
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
            Request(recv, self).cookies['s']
        )
    except KeyError:
        pass
    if recv['credentials'] is None:
        recv['credentials'] = {
            'email': 'Guest@hereus.net',
            'password': ''
        }
    if recv['credentials']['email'].split('@')[0] != 'Guest':
        print(f"\r(   ) {recv['credentials']['email']} [{datetime.now().strftime('%Y-%M-%d %H:%m:%S')}]",
              end=' ')
    print(f"{recv['method']} {recv['path']} {recv['protocol']}", end='', flush=True)
    if '?' in recv['path']:
        for i in recv['path'].split('?')[1].split('&'):
            recv['query'].update({i.split('=')[0]: i.split('=')[1]})
        # noinspection PyUnresolvedReferences
        recv['path'] = recv['path'].split('?')[0]
    return recv, client_socket
