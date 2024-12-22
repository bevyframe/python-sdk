from bevyframe.Helpers.Identifiers import https_codes


def send_in_chunks(sock, data, chunk_size):
    total_sent = 0
    c = b''
    while total_sent < len(data):
        chunk = data[total_sent:total_sent + chunk_size]
        try:
            sent = sock.send(chunk)
        except BrokenPipeError:
            break
        total_sent += sent
        c += chunk
    sock.send(b'')


def sender(_, recv, resp, client_socket, display_status_code):
    r = f"{recv['protocol']} {resp.status_code} {https_codes[resp.status_code]}\r\n"
    # r += "Transfer-Encoding: chunked\r\n"
    for header in resp.headers:
        r += f"{header}: {resp.headers[header]}\r\n"
    r += f"\r\n"
    r = r.encode()
    if not isinstance(resp.body, bytes):
        resp.body = resp.body.encode()
    try:
        client_socket.sendall(r)
    except BrokenPipeError:
        return
    # if b' 100 ' in client_socket.recv(4096):
    send_in_chunks(client_socket, resp.body, 4096)
    client_socket.close()
    print(f'\r({resp.status_code})' if display_status_code else '')
