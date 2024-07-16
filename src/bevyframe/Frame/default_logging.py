from typing import Any
from bevyframe.Objects.Request import Request


def default_logging(self, func) -> Any:
    self.default_logging_str = func

    def wrapper(r: Request, req_time: str) -> Any:
        return func(r, req_time)

    return wrapper
