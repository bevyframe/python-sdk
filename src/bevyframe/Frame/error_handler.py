import importlib.util
import importlib
import os
from bevyframe.Widgets.Page import Page
from bevyframe.Objects.Response import Response
from bevyframe.Helpers.Identifiers import *
from bevyframe.Widgets.Widget import Widget


def error_handler(self, request, status_code, exception) -> Response:
    # noinspection PyBroadException
    try:
        page_script_spec = importlib.util.spec_from_file_location(
            os.path.splitext(os.path.basename(f"./pages/{status_code}.py"))[0],
            f"./pages/{status_code}.py"
        )
        page_script = importlib.util.module_from_spec(page_script_spec)
        page_script_spec.loader.exec_module(page_script)
        resp = page_script.get(request)
        resp.status_code = status_code
        return resp
    except:
        t = exception.replace('\n', '<br>').split('<br>  File')
        e_boxes = [
            Widget(
                'h1',
                innertext=f'{https_codes[status_code]}'
            )
        ]
        if self.debug and status_code == 500:
            for e in t:
                if e.startswith('Traceback'):
                    e_boxes.append(
                        Widget(
                            'div',
                            style={'margin-bottom': '10px', 'padding-top': '10px', 'font-family': 'monospace'},
                            innertext=e
                        )
                    )
                elif 'site-packages' in e:
                    e_boxes.append(
                        Widget(
                            'div',
                            selector='the_box',
                            style={'margin-bottom': '10px', 'padding-top': '10px', 'font-family': 'monospace'},
                            innertext=(
                                    'Module ' +
                                    e.split('site-packages/')[1].split('/')[0] + ', ' +
                                    'file ' +
                                    e.split('site-packages/' + e.split('site-packages/')[1].split('/')[0] + '/')[
                                        1].split('"')[0] +
                                    e.removeprefix(e.split(',')[0])
                            )
                        )
                    )
                else:
                    e_boxes.append(
                        Widget(
                            'div',
                            selector='the_box',
                            style={'margin-bottom': '10px', 'padding-top': '10px', 'font-family': 'monospace'},
                            innertext=(
                                    'Path ' +
                                    e.split('"')[1].removeprefix('.').removesuffix('/__init__.py').removeprefix(
                                        os.getcwd()) +
                                    e.removeprefix(e.split('"')[0] + '"' + e.split('"')[1] + '"')
                            )
                        )
                    )
        try:
            return request.create_response(
                body=Page(
                    title=https_codes[status_code],
                    style=self.style,
                    childs=e_boxes,
                    color=request.user.id.settings.theme_color
                ).render(),
                status_code=status_code
            )
        except AttributeError:
            return request.create_response(
                body=Page(
                    title=https_codes[status_code],
                    style=self.style,
                    childs=e_boxes,
                    color="blank"
                ).render(),
                status_code=status_code
            )
