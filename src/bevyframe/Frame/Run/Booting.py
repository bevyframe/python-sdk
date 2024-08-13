import socket
import importlib.metadata


def booting(self, host: str, port: int, debug: bool):
    print(f"BevyFrame {importlib.metadata.version('bevyframe')} ⍺")
    print('Development server, do not use in production deployment')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f" * Serving BevyFrame app '{self.package}'")
    if debug or self.debug:
        self.debug = True
    print(f" * Debug mode: {'on' if self.debug else 'off'}")
    server_socket.bind((host, port))
    server_socket.listen(1)
    # noinspection HttpUrlsUsage
    print(f" * Running on http://{host}:{port}/".replace(":80/", "/").replace('://0.0.0.0', '://localhost'))
    print()
    return server_socket
