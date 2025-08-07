from types import *
from bevystyle.RenderCSS import RenderCSS

m = {
    'Label': 'p',
    'Textbox': '.textbox',
    'Button': '.button',
    'SmallButton': '.button.small',
    'MiniButton': '.button.mini',
    'Link': 'a',
    'TextArea': 'textarea',
    'Page': 'body',
    'Box': '.the_box',
    'Navbar': 'nav.Navbar',
    'Topbar': 'nav.Topbar',
}


def compile_style(
        backend: bool = False,
        css: dict = None,
        color: str = None,
        background_color: str = None,
        background_image: str = None,
        aspect_ratio: float = None,
        height: str = None,
        width: str = None,
        min_height: str = None,
        max_height: str = None,
        min_width: str = None,
        max_width: str = None,
        text_align: str = None,
        align_items: str = None,
        margin = None,
        padding = None,
        position = None,
        border_radius: str = None,
        font_size: str = None,
        vertical_align: str = None,
        cursor: str = None,
        text_decoration: str = None,
        border: str = None,
        outline: str = None,
        font_weight: int = None,
        z_index: int = None,
        font_family: list = None,
        overflow = None,
        scroll_behavior: str = None,
        accent_color: str = None,
        backdrop_filter: str = None,
        filter: str = None,
        visibility: str = None,
        **kwargs
) -> dict:
    d = {}
    if css is not None:
        d = css
    if background_image is not None:
        d['background-attachment'] = 'fixed'
        d['background-image'] = f"url('{background_image}')" if '(' not in background_image else background_image
    if isinstance(margin, str):
        d.update({'margin': margin})
    elif hasattr(margin, 'type') and margin.type() == 'margin':
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(margin, i) is not None:
                d.update({f'margin-{i}': getattr(margin, i)})
    if isinstance(padding, str):
        d.update({'padding': padding})
    elif hasattr(padding, 'type') and padding.type() == 'padding':
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(padding, i) is not None:
                d.update({f'padding-{i}': getattr(padding, i)})
    if hasattr(position, 'type') and position.type() == 'position':
        d.update({'position': position.item})
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(position, i) is not None:
                d.update({i: getattr(position, i)})
    if isinstance(overflow, str):
        d.update({'overflow': overflow})
    elif hasattr(overflow, 'type') and overflow.type() == 'overflow':
        for i in ['x', 'y']:
            if getattr(overflow, i) is not None:
                d.update({f'overflow-{i}': getattr(overflow, i)})
    if isinstance(border_radius, str):
        d.update({'border-radius': border_radius})
    elif border_radius and hasattr(border_radius, 'type') and border_radius.type() == 'border_radius':
        for i in ['top_left', 'top_right', 'bottom_left', 'bottom_right']:
            if getattr(border_radius, i) is not None:
                d.update({f'border-{i}-radius'.replace('_', '-'): getattr(border_radius, i)})
    if isinstance(border, str):
        d.update({'border': border})
    k = [i for i in locals().keys()]
    for i in k:
        obj_blacklist = [
            'self', 'item', 'style', 'css', 'data', 'element', 'content', 'margin', 'padding', 'position', 'kwargs',
            'd', 'backend', 'i', 'overflow', 'background_image', 'background_attachment', 'border_radius',
        ]
        if i not in obj_blacklist and locals()[i] is not None and not i.startswith('__'):
            if backend:
                d.update({i.replace('_', '-'): 'none' if locals()[i] is None else locals()[i]})
            else:
                d.update({i.replace('_', '-'): f"{'none' if locals()[i] is None else locals()[i]} !important"})
    return d


def compiler_bridge(source: dict) -> tuple:
    d = {
        'nav.Navbar a button': {
            'border': 'none',
            'background-color': 'transparent',
            'padding-top': '14px',
            'padding-right': '16px',
            'padding-bottom': '14px',
            'padding-left': '16px',
            'align-items': 'left',
            'border-radius': '15px',
            'cursor': 'pointer'
        }
    }
    light = {}
    dark = {}
    mobile = {}
    desktop = {}
    imports = []
    for val1 in source:
        if val1 == 'imports':
            imports = [str(i) for i in source[val1]]
        elif val1 == 'webkit':
            for i in source[val1]:
                d[f'::-webkit-{i}'] = compile_style(backend=True, css=source[val1][i])
        else:
            if isinstance(source[val1], type):
                val1_d = source[val1].__dict__
                if val1 in m:
                    d[m[val1]] = compile_style(backend=True, **val1_d)
                    if 'LightTheme' in val1_d:
                        val1_d_l = val1_d['LightTheme'].__dict__
                        light[m[val1]] = compile_style(backend=True, **val1_d_l)
                        for i in ['Blank', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Pink']:
                            if i in val1_d_l:
                                tag = f".body_{i.lower()}" if val1 == 'Page' else f"body.body_{i.lower()} {m[val1]}"
                                light[tag] = compile_style(backend=True, **val1_d_l[i].__dict__)
                    if 'DarkTheme' in val1_d:
                        val1_d_l = val1_d['DarkTheme'].__dict__
                        dark[m[val1]] = compile_style(backend=True, **val1_d_l)
                        for i in ['Blank', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Pink']:
                            if i in val1_d_l:
                                tag = f".body_{i.lower()}" if val1 == 'Page' else f"body.body_{i.lower()} {m[val1]}"
                                dark[tag] = compile_style(backend=True, **val1_d_l[i].__dict__)
                    if 'Hover' in val1_d:
                        d[f'{m[val1]}:hover'] = compile_style(backend=True, **val1_d['Hover'].__dict__)
                    if 'Focus' in val1_d:
                        d[f'{m[val1]}:focus'] = compile_style(backend=True, **val1_d['Focus'].__dict__)
                    if 'Mobile' in val1_d:
                        val1_d_l = val1_d['Mobile'].__dict__
                        mobile[m[val1]] = compile_style(backend=True, **val1_d_l)
                    if 'Desktop' in val1_d:
                        val1_d_l = val1_d['Desktop'].__dict__
                        desktop[m[val1]] = compile_style(backend=True, **val1_d_l)
                elif val1 == 'Badge' and 'Caution' in val1_d:
                    val1_d_l = val1_d['Caution'].__dict__
                    d['.caution::after'] = compile_style(backend=True, **val1_d_l)
                if val1 == 'Navbar':
                    if 'RawItem' in val1_d:
                        val1_d_l = val1_d['RawItem'].__dict__
                        d['nav.Navbar a button'] = compile_style(backend=True, **val1_d_l)
                        if 'color' in val1_d_l:
                            if isinstance(val1_d_l['color'], list):
                                light[f'nav.Navbar a button span'] = compile_style(backend=True, color=val1_d_l['color'][0])
                                dark[f'nav.Navbar a button span'] = compile_style(backend=True, color=val1_d_l['color'][1])
                            else:
                                d[f'nav.Navbar a button span'] = compile_style(backend=True, color=val1_d_l['color'])
                    for i in ['Active', 'Inactive']:
                        if f'{i}Item' in val1_d:
                            val1_d_l = val1_d[f'{i}Item'].__dict__
                            d[f'nav.Navbar a.{i.lower()} button'] = compile_style(backend=True, **val1_d_l)
                            if 'color' in val1_d_l:
                                if isinstance(val1_d_l['color'], list):
                                    light[f'nav.Navbar a.{i.lower()} button span'] = compile_style(backend=True, color=val1_d_l['color'][0])
                                    dark[f'nav.Navbar a.{i.lower()} button span'] = compile_style(backend=True, color=val1_d_l['color'][1])
                                else:
                                    d[f'nav.Navbar a.{i.lower()} button span'] = compile_style(backend=True, color=val1_d_l['color'])
    d.update({'@media (prefers-color-scheme: light)': light})
    d.update({'@media (prefers-color-scheme: dark)': dark})
    d.update({f'@media (min-width: 768px)': desktop})
    d.update({f'@media (max-width: 768px)': mobile})
    return imports, d


def compile_object(obj) -> str:
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return RenderCSS(obj)
    elif isinstance(obj, type):
        listed = {k: obj.__dict__[k] for k in obj.__dict__ if not k.startswith("__")}
    elif isinstance(obj, ModuleType):
        listed = {k: getattr(obj, k) for k in dir(obj) if not k.startswith("__")}
    else:
        return ""
    imports, d = compiler_bridge(listed)
    imports = " ".join([f"@import url('{i}');" for i in imports])
    compiled = (RenderCSS(d)
                .replace('  ', ' ')
                .replace(' { ', '{')
                .replace('; } ', ';}')
                .replace('{} ', '{}'))
    return imports + compiled + (listed['css'] if 'css' in listed else "")
