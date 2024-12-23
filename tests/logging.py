from datetime import datetime, UTC
from bevyframe import *
from models import Test


def logging(context: Context, time: str) -> (str, tuple[str, bool]):
    context.db.add(Test(email=context.email, ip=context.ip, when=datetime.now(UTC)))
    context.db.commit()
    u = context.email
    if u.split('@')[0] == 'Guest':
        u = context.ip
    if context.path in ['/favicon.png']:
        last = context.db.query(Test).order_by(Test.id).all()[-1]
        end = f" at {time.split(' ')[0]} on {time.split(' ')[1]}" if last.email != context.email and last.ip != context.ip else ''
        return f"{''.join([' ' for _ in range(len(u))])} and requested {context.path}{end}", False
    else:
        return f"{u} {'sent form to' if context.method == 'POST' else 'loaded'} {context.path} at {time.split(' ')[0]} on {time.split(' ')[1]}"
