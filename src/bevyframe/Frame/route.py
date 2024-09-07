from typing import Any
from bevyframe.Objects.Context import Context


def route(self, path, whitelist: list = None, blacklist: list = None) -> Any:
    def decorator(func) -> Any:
        self.routes.update({path: func})

        def wrapper(r: Context, **others) -> Any:
            if whitelist is not None:
                if r.email not in whitelist:
                    return self.error_handler(r, 401, '')
            elif blacklist is None:
                if r.email in blacklist:
                    return self.error_handler(r, 401, '')
            return func(r, **others)

        return wrapper

    return decorator
