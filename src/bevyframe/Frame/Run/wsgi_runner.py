from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlsplit
import logging
from wsgiref.simple_server import WSGIServer

logging.getLogger("http.server").setLevel(logging.CRITICAL)


# noinspection PyUnresolvedReferences
class WSGIHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.handle_request()

    def do_POST(self) -> None:
        self.handle_request()

    def handle_request(self) -> None:
        environ = {
            "REQUEST_METHOD": self.command,
            "PATH_INFO": urlsplit(self.path).path,
            "QUERY_STRING": urlsplit(self.path).query,
            "CONTENT_TYPE": self.headers.get("Content-Type", ""),
            "CONTENT_LENGTH": self.headers.get("Content-Length", "0"),
            "SERVER_NAME": self.server.server_name,
            "SERVER_PORT": str(self.server.server_port),
            "REMOTE_ADDR": self.client_address[0],  # Client IP address
            "wsgi.input": BytesIO(self.rfile.read(int(self.headers.get("Content-Length", "0")))),
            "wsgi.errors": None,
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
        }
        for key in self.headers:
            environ[f"HTTP_{key}"] = self.headers.get(key)
        status = ""
        headers = []
        response_body = []
        def start_response(status_line, response_headers) -> callable:
            nonlocal status, headers
            status = status_line
            headers = response_headers
            return response_body.append
        response_body = self.server.wsgi_app(environ, start_response)
        status_code, status_text = status.split(" ", 1)
        self.send_response(int(status_code), status_text)
        for header_name, header_value in headers:
            self.send_header(header_name, header_value)
        self.end_headers()
        for chunk in response_body:
            self.wfile.write(chunk)

    def log_message(self, _, *args) -> None:
        pass


def make_server(wsgi_app: callable, host: str, port: int) -> WSGIServer:
    class WSGIServer(HTTPServer):
        def __init__(self, server_address, request_handler_class, wsgi_app) -> None:
            super().__init__(server_address, request_handler_class)
            self.wsgi_app = wsgi_app
    return WSGIServer((host, port), WSGIHandler, wsgi_app)
