from datetime import datetime
import mimetypes
import socket
import urllib
import time
import os

class request:
    status_code = 0
    cookies = {}
    method = ''
    form = {}

class Frame:
    def __init__(self, routes, paths):
        self.routes = routes
        self.paths = paths
    def handle_request(self, client_socket, client_address):
        request_data = client_socket.recv(1024).decode()
        request_lines = request_data.split('\r\n')
        request_line = request_lines[0]
        request.method, path, _ = request_line.split(' ')
        for header in request_lines[1:]:
            if ':' in header:
                key, value = header.split(': ', 1)
                if key.lower() == 'cookie':
                    cookie_list = value.split('; ')
                    for cookie in cookie_list:
                        cookie_key, cookie_value = cookie.split('=')
                        request.cookies[cookie_key] = cookie_value
        if request.method == 'POST':
            content_length = 0
            for header in request_lines[1:]:
                if header.lower().startswith('content-length:'):
                    content_length = int(header.split(': ')[1])
                    break
            form_data_str = request_data.split('\r\n\r\n', 1)[1][:content_length]
            request.form = urllib.parse.parse_qs(form_data_str)
        if path.startswith('/static/') or path.startswith('/Files/'):
            try:
                response_data = 'HTTP/1.1 200 OK\r\nContent-Type: '.encode()+mimetypes.types_map.get('.'+path.split('.')[-1], "application/octet-stream").encode()+'\r\n\r\n'.encode()+open('./Files/'+path.removeprefix('/'+path.split('/')[1]+'/'), 'rb').read(); request.status_code = 200
            except Exception as e:
                try: response_data = '\r\n\r\n'+self.routes.__error_page__(500); request.status_code = 500; print(e)
                except: response_data = '\r\n\r\n<h1>500 Internal Server Error</h1>'+str(e); request.status_code = 500; print(e)
                for cookie in request.cookies: response_data = cookie+'='+request.cookies[cookie]+'; '+response_data
                response_data = 'HTTP/1.1 '+str(request.status_code)+' OK\r\nContent-Type: text/html\r\n'+response_data
                response_data = response_data.encode()
        else:
            if path in self.paths:
                try:
                    response_data = self.paths[path][0](**self.paths[path][1]); request.status_code = 200
                except Exception as e:
                    try: response_data = self.routes.__error_page__(500); request.status_code = 500; print(e)
                    except: response_data = '<h1>500 Internal Server Error</h1>'+str(e); request.status_code = 500; print(e)
            else:
                try: response_data = self.routes.__error_page__(404); request.status_code = 404
                except: response_data = '<h1>404 Not Found</h1>'; request.status_code = 404
            response_data = '\r\n\r\n'+response_data
            for cookie in request.cookies: response_data = cookie+'='+request.cookies[cookie]+'; '+response_data
            response_data = 'HTTP/1.1 '+str(request.status_code)+' OK\r\nContent-Type: text/html\r\n'+response_data
            response_data = response_data.encode()
        print(f'{str(datetime.utcnow()).split(".")[0]} [{client_address[0]}:{client_address[1]}] {request.status_code} {request.method} {path}')
        client_socket.sendall(response_data)
        request.cookies = {}
        request.method = ''
        request.form = {}
        client_socket.close()
    def start_server(self, host='127.0.0.1', port=5000, debug=False):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print('BevyFrame Preview Release 0.1')
        print('Downstream Version, Do Not Use in Production')
        print(f'App is live on http://{host}:{port}')
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                self.handle_request(client_socket, client_address)
        except KeyboardInterrupt: server_socket = None; print('\nServer Killed!')
    def run(self):
        self.start_server(host='0.0.0.0', port=8000, debug=False)

def renderpage(html, **variables):
    template = open('./Pages/'+html, 'r', encoding='UTF-8').read()
    for variable in variables:
        template = template.replace('{{'+variable+'}}', str(variables[variable]))
    return template

def redirect(url): return '<meta http-equiv="Refresh" content="0; url='+"'"+url+"'"+'" />'

from .widgets import Widget