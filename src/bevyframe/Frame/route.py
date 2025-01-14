from bevyframe.Objects.Context import Context


def route(self, path, whitelist: list = None, blacklist: list = None) -> callable:
    def decorator(func) -> callable:
        self.routes.update({path: func})
        def wrapper(r: Context, **others) -> any:
            if whitelist is not None:
                if r.email not in whitelist:
                    return self.error_handler(r, 401, '')
            elif blacklist is None:
                if r.email in blacklist:
                    return self.error_handler(r, 401, '')
            return func(r, **others)
        return wrapper
    return decorator
