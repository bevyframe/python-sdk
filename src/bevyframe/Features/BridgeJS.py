import os


def client_side_bridge() -> str:
    functions = '''
        const _bridge = (func, ...args) => {
            fetch(`${location.protocol}//${location.host}/.well-known/bevyframe/proxy`,{
                method:'POST',headers:{'Content-Type':'application/json'},
                credentials: 'include',
                body: JSON.stringify({func:func,args:args,path:window.location.pathname}),
            }).then(res => res.json()).then(data => {
                if (data.error) {throw new Error(data.error);}
                else if (data.type === 'return') {return data.value;}
                else if (data.type === 'script') {eval(data.value);}
                else if (data.type === 'view') {
                    if (data.element === 'body') {document.body.innerHTML = data.value;}
                    else {document.querySelector(data.element).innerHTML = data.value;}
                }
            }).catch(err => {  });
        };
    '''
    for i in os.listdir('./functions/'):
        if i.endswith('.py'):
            i = i[:-3]
            functions += " const " + i + " = (...args) => {_bridge('" + i + "', ...args)};"
    functions = (functions
                 .replace('    ', '')
                 .replace('  ', ' ')
                 .replace('\n', '')
                 .strip())
    return functions
