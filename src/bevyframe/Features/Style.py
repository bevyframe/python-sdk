from types import *
import re
from bevyframe.Helpers.RenderCSS import RenderCSS
from bevyframe.Widgets.Style import *

m = {
    'Label': 'p',
    'Textbox': '.textbox',
    'Button': '.button',
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
        height: str = None,
        width: str = None,
        min_height: str = None,
        max_height: str = None,
        min_width: str = None,
        max_width: str = None,
        text_align: str = None,
        align_items: str = None,
        margin: (str, Margin) = None,
        padding: (str, Padding) = None,
        position: (Position.fixed, Position.sticky, Position.absolute, Position.relative) = None,
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
        overflow: Overflow = None,
        scroll_behavior: str = None,
        accent_color: str = None,
        backdrop_filter: str = None,
        filter: str = None,
        **kwargs
) -> dict:
    d = {}
    if css is not None:
        d = css
    if isinstance(margin, str):
        d.update({'margin': margin})
    elif isinstance(margin, Margin):
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(margin, i) is not None:
                d.update({f'margin-{i}': getattr(margin, i)})
    if isinstance(padding, str):
        d.update({'padding': padding})
    elif isinstance(padding, Padding):
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(padding, i) is not None:
                d.update({f'padding-{i}': getattr(padding, i)})
    if isinstance(position, (Position.fixed, Position.sticky, Position.absolute, Position.relative)):
        d.update({'position': position.item})
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(position, i) is not None:
                d.update({i: getattr(position, i)})
    if isinstance(overflow, Overflow):
        for i in ['x', 'y']:
            if getattr(overflow, i) is not None:
                d.update({f'overflow-{i}': getattr(overflow, i)})
    elif isinstance(overflow, str):
        d.update({'overflow': overflow})
    if isinstance(border, FourSided):
        for i in ['top', 'right', 'bottom', 'left']:
            if getattr(border, i) is None:
                d.update({f'border-{i}': 'none'})
            else:
                d.update({f'border-{i}': getattr(border, i)})
    elif isinstance(border, str):
        d.update({'border': border})
    k = [i for i in locals().keys()]
    for i in k:
        obj_blacklist = ['self', 'item', 'style', 'css', 'data', 'element', 'content', 'margin', 'padding', 'position', 'kwargs', 'd', 'backend', 'i', 'overflow', 'border']
        if i not in obj_blacklist and locals()[i] is not None and not i.startswith('__'):
            if backend:
                d.update({i.replace('_', '-'): 'none' if locals()[i] is None else locals()[i]})
            else:
                d.update({i.replace('_', '-'): f"{'none' if locals()[i] is None else locals()[i]} !important"})
    return d


def compiler_bridge(c: str, source: dict, d: dict, light_theme: dict, dark_theme: dict, mobile: dict, desktop: dict) -> tuple:
    for j in source:
        if j == 'webkit':
            for i in source[j]:
                d[f'::-webkit-{i}'] = source[j][i]
        elif j in m:
            y: dict = {k: source[j].__dict__[k] for k in source[j].__dict__ if not k.startswith("__")}
            for i in y:

                if i in ['Hover', 'Focus']:
                    z = y[i].__dict__
                    kwargs = {k: z[k] for k in z if not k.startswith('__')}
                    d[f'{m[j]}:{i.lower()}'] = compile_style(backend=True, **kwargs)

                elif i == 'LightTheme':
                    light_theme.update({j: y[i]})
                elif i == 'DarkTheme':
                    dark_theme.update({j: y[i]})
                elif i == 'Mobile':
                    mobile.update({j: y[i]})
                elif i == 'Desktop':
                    desktop.update({j: y[i]})

                elif c != 'main' and i in ['Blank', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Pink']:
                    z = y[i].__dict__
                    for k in z:
                        if isinstance(z[k], type):
                            q = z[k].__dict__
                            kwargs = {g: q[g] for g in q if not g.startswith('__')}
                            for o in ['background_color', 'color']:
                                for l in ['active', 'inactive']:
                                    if f'{l}_item_{o}' in kwargs and j == 'Navbar':
                                        if f'nav.Navbar a.{l} button' not in d:
                                            d[f'nav.Navbar a.{l} button'] = {}
                                        d[f'nav.Navbar a.{l} button' + (' font' if 'b' not in o else '')][o] = kwargs[f'{l}_item_{o}']
                            d[f'.body_{i.lower()} {m[j]}.{k.lower()}'] = compile_style(backend=True, **kwargs)
                    kwargs = {k: z[k] for k in z if not isinstance(z[k], type) and not k.startswith('__')}
                    d[f'.body_{i.lower()} {m[j]}'.removesuffix(' body')] = compile_style(backend=True, **kwargs)

                elif j == 'Navbar' and i in ['ActiveItem', 'InactiveItem']:
                    z = y[i].__dict__
                    kwargs = {k: z[k] for k in z if not k.startswith('__')}
                    d[f'nav.Navbar a.{i.lower().removesuffix("item")} button'] = compile_style(backend=True, **kwargs)
                    if 'color' in z:
                        d[f'nav.Navbar a.{i.lower().removesuffix("item")} button span'] = compile_style(backend=True, color=z['color'])
                elif j == 'Navbar' and i == 'RawItem':
                    z = y[i].__dict__
                    kwargs = {k: z[k] for k in z if not k.startswith('__')}
                    d[f'nav.Navbar a'] = compile_style(backend=True, **kwargs)

                elif j == 'Topbar' and i == 'Item':
                    z = y[i].__dict__
                    kwargs = {k: z[k] for k in z if not k.startswith('__')}
                    d[f'nav.Topbar a button'] = compile_style(backend=True, **kwargs)
                    if 'color' in z:
                        d[f'nav.Topbar a button span'] = compile_style(backend=True, color=z['color'])

                elif isinstance(y[i], type) and c == 'main':
                    z = y[i].__dict__
                    kwargs = {k: z[k] for k in z if not k.startswith('__')}
                    d[f"{m[j]}.{re.sub(r'(?<!^)(?=[A-Z])', '_', i).lower()}"] = compile_style(backend=True, **kwargs)

                kwargs = {k: y[k] for k in y if not isinstance(y[k], type) and not k.startswith('__')}
                d[f'{m[j]}'] = compile_style(backend=True, **kwargs)

        elif j == 'Badge':
            if 'Caution' in source[j].__dict__:
                z = source[j].Caution.__dict__
                kwargs = {k: z[k] for k in z if not isinstance(z[k], type) and not k.startswith('__')}
                d['.caution::after'] = compile_style(backend=True, **kwargs)

    return d, light_theme, dark_theme, mobile, desktop


def compile_object(obj) -> str:
    r = {}
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
    mobile = {}
    desktop = {}
    light_theme = {}
    dark_theme = {}
    for c in ['main', 'mobile', 'desktop', 'light', 'dark']:
        d = {}
        source = {'main': listed, 'light': light_theme, 'dark': dark_theme, 'mobile': mobile, 'desktop': desktop}[c]
        if 'imports' in source:
            d['@imports'] = source['imports']
        d, light_theme, dark_theme, mobile, desktop = compiler_bridge(c, source, d, light_theme, dark_theme, mobile, desktop)
        if c == 'main':
            r = d
        elif c in ['light', 'dark']:
            r.update({f'@media (prefers-color-scheme: {c})': d})
        elif c in ['mobile', 'desktop']:
            r.update({f'@media ({"min" if c == "desktop" else "max"}-width: 768px)': d})
    return RenderCSS(r).replace('  ', ' ').replace(' { ', '{').replace('; } ', ';}').replace('{} ', '{}')
