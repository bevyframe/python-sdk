from bevyframe import *
import secrets
import sys

config = {
    'host': '127.0.0.1',
    'port': 5000,
    'debug': True,
    'package': 'dev.islekcaganmert.bevyframe.stdin',
    'administrator': 'islekcaganmert@hereus.net',
    'developer': 'islekcaganmert@hereus.net',
    'style': {},
    'keywords': []
}
if len(sys.argv) == 2:
    c = json.load(open(sys.argv[1], 'rb'))
    for i in c:
        config[i] = c[i]
elif len(sys.argv) == 3:
    config['host'], config['port'] = sys.argv[1], int(sys.argv[2])
Frame(
    config['package'],
    config['developer'],
    config['administrator'],
    secrets.token_hex(secrets.randbits(4)),
    config['style'],
    '/favicon.ico',
    config['keywords']
).run(
    host=config['host'],
    port=config['port'],
    debug=config['debug']
)
