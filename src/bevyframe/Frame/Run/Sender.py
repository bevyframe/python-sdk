from bevyframe.Helpers.Identifiers import https_codes


def sender(self, recv, resp, client_socket):
    r = f"{recv['protocol']} {resp.status_code} {https_codes[resp.status_code]}\r\n"
    for header in resp.headers:
        r += f"{header}: {resp.headers[header]}\r\n"
    r += f"\r\n"
    r = r.encode()
    if not isinstance(resp.body, bytes):
        resp.body = resp.body.encode()
    r += resp.body
    client_socket.sendall(r)
    client_socket.close()
    print(f'\r({resp.status_code})')
