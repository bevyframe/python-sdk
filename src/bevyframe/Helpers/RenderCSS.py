def RenderCSS(style: (str, dict)) -> str:
    if isinstance(style, str):
        return style
    css = ''
    for prop in style:
        if prop.startswith('@'):
            if prop == '@imports':
                for i in style[prop]:
                    css += f"@import url('{i}'); "
            else:
                f = ''
                while True:
                    try:
                        for inprop in style[prop]:
                            if inprop.startswith('@'):
                                f = f'({inprop.removeprefix("@")}: {style[prop][inprop]})'
                                style[prop].pop(inprop)
                        break
                    except KeyError or AttributeError or ValueError or TypeError or IndexError or Exception:
                        pass
                css += f'{prop} {f} '
                css += ('{ ' + RenderCSS(style[prop]) + '}')
        elif isinstance(style[prop], list):
            css += f'{prop}:{", ".join(style[prop])};'
        elif isinstance(style[prop], str):
            css += f'{prop}:{style[prop]};'
        elif isinstance(style[prop], int):
            css += f'{prop}:{style[prop]};'
        elif isinstance(style[prop], list):
            css += f'{prop}:{", ".join(style[prop])};'
        else:
            css += f'{prop} '
            css += ('{ ' + RenderCSS(style[prop]) + '}')
        css += ' '
    return css
