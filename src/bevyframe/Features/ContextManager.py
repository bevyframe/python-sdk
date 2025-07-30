import pickle
import socket


def get_from_context_manager(package: str, email: str, name: str) -> any:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect(f"/opt/bevyframe/sockets/{package}")
    sock.sendall(f"get {email} {name}".encode())
    cmd = sock.recv(4096).decode().removesuffix('\n')
    tp, ln = cmd.split(" ", 1)
    ln = int(ln)
    data = b""
    sock.sendall(b"OK")
    while len(data) < ln:
        data += sock.recv(4096)
    if tp == "string":
        return data.decode()
    elif tp == "char":
        return data.decode()[1:]
    elif tp == "integer":
        return int(data.decode())
    elif tp == "float":
        return float(data.decode())
    elif tp == "boolean":
        return bool(data.decode())
    elif tp == "python":
        return pickle.loads(data)
    elif tp == "null":
        return None
    return data


def set_to_context_manager(package: str, email: str, name: str, data: any) -> int:
    if isinstance(data, str):
        tp = "string"
        data = data.encode()
    elif isinstance(data, int):
        tp = "integer"
        data = str(data).encode()
    elif isinstance(data, float):
        tp = "float"
        data = str(data).encode()
    elif isinstance(data, bool):
        tp = "boolean"
        data = "true".encode() if data else "false".encode()
    else:
        tp = "python"
        data = pickle.dumps(data)
    ln = len(data)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect(f"/opt/bevyframe/sockets/{package}")
    sock.sendall(f"set {email} {tp} {name} {ln}".encode())
    sock.recv(4096)
    sock.sendall(data)
    return int(sock.recv(4096).decode())
