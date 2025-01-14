from bevyframe.Objects.Context import Context


def default_logging(self, func: callable) -> callable:
    self.default_logging_str = func
    def wrapper(r: Context, req_time: str) -> callable:
        return func(r, req_time)
    return wrapper
