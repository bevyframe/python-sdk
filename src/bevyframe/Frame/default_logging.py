from typing import Any
from bevyframe.Objects.Context import Context


def default_logging(self, func) -> Any:
    self.default_logging_str = func

    def wrapper(r: Context, req_time: str) -> Any:
        return func(r, req_time)

    return wrapper
