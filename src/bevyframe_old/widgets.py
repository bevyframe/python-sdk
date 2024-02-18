def Widget(element, **kwargs):
    htmlgen = f'<{element}'
    for arg in kwargs:
        if arg in ['childs','innertext']:
            pass
        elif arg == 'style':
            cssgen = ''
            for prop in kwargs[arg]:
                cssgen+=f'{prop}:{kwargs[arg][prop]};'
            htmlgen+=f' {arg}="{cssgen}"'
        else:
            htmlgen+=f' {arg}="{kwargs[arg]}"'
    htmlgen+='>'
    if 'childs' in kwargs:
        for child in kwargs['childs']:
            htmlgen+=child
    elif 'innertext' in kwargs:
        htmlgen+=str(kwargs['innertext'])
    htmlgen+=f'</{element}>'
    return htmlgen