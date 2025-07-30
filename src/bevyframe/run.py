import io
import json
import os
import subprocess
import sys
import importlib.util
import traceback
from bevyframe.Features.Bridge import JavaScript, change_html
from bevyframe.Features.ErrorHandler import error_handler, Error404, Error401
from bevyframe.Objects.Context import Context
from bevyframe.Objects.Response import Response
from bevyframe.Widgets.Page import Page


def run() -> int:
    file_path = sys.argv[1]
    sys.path += [os.getcwd()]
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

    resp_body = []
    status_code = ''
    resp_headers = []
    http_headers = {}
    http_query = {}
    environ = {
        'REQUEST_METHOD': req_headers.get('Method', 'GET'),
        'PATH_INFO': req_headers.get('Path', '/'),
        'REMOTE_ADDR': req_headers.get('IP', '127.0.0.1'),
        'QUERY_STRING': '',
        'wsgi.input': io.BytesIO(req_body),
        'wsgi.url_scheme': 'https'
    }

    for i in req_headers:
        if i.startswith('Header.'):
            environ.update({"HTTP_" + i.removeprefix('Header.').upper(): req_headers[i]})
            http_headers.update({i.removeprefix('Header.'): req_headers[i]})
        elif i.startswith('Query.'):
            http_query.update({i.removeprefix('Query.'): req_headers[i]})

    def start_response(status: str, _headers: list[tuple[str, str]]) -> callable:
        nonlocal status_code, resp_headers
        status_code = status.split(' ', 1)[0]
        resp_headers = _headers
        return resp_body.append

    permissions = req_headers.get('Permissions', '').split(',')
    if not any(permissions):
        permissions = []
    r = Context({
        'method': req_headers.get('Method', 'GET'),
        'path': req_headers.get('Path', '/'),
        'protocol': 'bevyframe',
        'headers': http_headers,
        'body': req_body,
        'credentials': {
            'email': req_headers['Cred.Email'],
            'token': req_headers['Cred.Token'],
            'username': req_headers['Cred.Username'],
            'network': req_headers['Cred.Network'],
        },
        'query': http_query,
        'ip': req_headers.get('IP', '127.0.0.1'),
        'permissions': permissions,
        'package': req_headers.get('Package'),
        'loginview': req_headers.get('LoginView'),
    })

    resp = None

    try:
        page_script_spec = importlib.util.spec_from_file_location(
            os.path.splitext(os.path.basename(file_path))[0],
            file_path
        )
        page_script = importlib.util.module_from_spec(page_script_spec)
        page_script_spec.loader.exec_module(page_script)

        if 'whitelist' in page_script.__dict__:
            if r.email not in page_script.whitelist():
                resp = error_handler(r, 401, '')
        elif 'blacklist' in page_script.__dict__:
            if r.email in page_script.blacklist():
                resp = error_handler(r, 401, '')
        if file_path.split('/')[-2] == 'functions':
            func_name = file_path.split('/')[-1]
            func_name = func_name.removesuffix("." + func_name.split('.')[-1])
            if func_name in page_script.__dict__:
                try:
                    args = json.loads(r.body)
                    retval = getattr(page_script, func_name)(r, *args)
                    if isinstance(retval, JavaScript):
                        retval = {'type': 'script', 'value': str(retval.script)}
                    elif isinstance(retval, change_html):
                        retval = {'type': 'view', 'value': retval.html, 'element': retval.tag}
                    elif type(retval).__name__ == 'Page':
                        retval = {'type': 'view', 'value': retval.bf_widget(), 'element': 'html'}
                    else:
                        retval = {'type': 'return', 'value': str(retval)}
                    resp = r.create_response(body=retval)
                except:
                    resp = r.create_response(
                        body={
                            "error": traceback.format_exc()
                        }
                    )
        elif 'application' in page_script.__dict__:
            resp_body += page_script.application(environ, start_response)
        elif r.method.lower() in page_script.__dict__:
            try:
                resp = getattr(page_script, r.method.lower())(r)
            except:
                resp = error_handler(r, 500, traceback.format_exc())
        elif 'application/activity+json' == http_headers.get('Accept', '').split(';')[0]:
            if 'activity' in page_script.__dict__:
                pass
        else:
            resp_body = [b'ERROR, not wsgi, not bevyframe', environ['REQUEST_METHOD'].lower().encode()]
            environ.pop('wsgi.input')
            resp_body += [json.dumps(environ).encode()]
            resp_body += [json.dumps([i for i in page_script.__dict__]).encode()]
            status_code = '500'
            resp_headers = [('Content-Type', 'text/plain')]

    except Error404:
        resp = error_handler(r, 404, '')

    except Error401:
        resp = error_handler(r, 401, '')

    except:
        resp = error_handler(r, 500, traceback.format_exc())

    if resp:
        if isinstance(resp, Page):
            resp = r.create_response(resp, headers={'Content-Type': 'application/bevyframe'})
        if not isinstance(resp, Response):
            resp = r.create_response(resp)

        if isinstance(resp.body, str) or isinstance(resp.body, int):
            resp.body = str(resp.body).encode()
        elif isinstance(resp.body, list) or isinstance(resp.body, dict):
            resp.body = json.dumps(resp.body).encode()
            if resp.headers['Content-Type'] == 'text/html; charset=utf-8':
                resp.headers['Content-Type'] = 'application/json'
        elif isinstance(resp.body, Page):
            resp.body = resp.body.stdout().encode()

        resp_body = [resp.body]
        status_code = str(resp.status_code)
        resp_headers = resp.headers.items()

    out = f"BevyFrame {status_code}\n".encode()
    for header in resp_headers:
        out += f"{header[0]}: {header[1]}\n".encode()
    if 'email' in resp.credentials and 'token' in resp.credentials:
        out += f"Cred-Email: {resp.credentials['email']}\n".encode()
        out += f"Cred-Token: {resp.credentials['token']}\n".encode()
    else:
        out += f"No-Cred: 1\n".encode()
    out += b'\n'
    for line in resp_body:
        out += line + b'\n'
    out += b'\n'
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    return 0


def application(environ, start_response):
    header_name_capitalize = lambda name: '-'.join(part.lower().capitalize() for part in name.removeprefix('HTTP_').split('_'))
    simulatable = {
        "method": environ.get('REQUEST_METHOD', 'GET'),
        "path": environ.get('PATH_INFO', '/'),
        "headers": {
            header_name_capitalize(k): v
            for k, v in environ.items() if k.startswith('HTTP_')
        },
        "body": environ['wsgi.input'].read().hex(),
    }
    simulatable_str = json.dumps(simulatable)
    try:
        result_raw = subprocess.check_output(
            [f"{os.environ.get('BEVYFRAME_INSTALLATION', '/opt/bevyframe')}/bin/bevyframe", "simulate_request"],
            input=simulatable_str.encode(),  # pass bytes
        )
    except subprocess.CalledProcessError as e:
        result_raw = e.output
    try:
        result = json.loads(result_raw.decode())
    except json.JSONDecodeError:
        result = {
            'status_code': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f"Error decoding JSON response: {result_raw.decode()}"
        }
    start_response(str(result['status_code']), list(result['headers'].items()))
    return [result['body'].encode()]
