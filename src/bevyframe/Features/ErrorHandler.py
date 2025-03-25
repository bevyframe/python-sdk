from bevyframe.Objects.Response import Response


class Error404(Exception):
    """Raised when a page is not found"""
    pass


class Error401(Exception):
    """Raised when a page is not found"""
    pass


def error_handler(request, status_code: int, exception: str) -> Response:
    if status_code == 500:
        return request.create_response(
            body=f"Response.Type: Error\n\n{exception}\n",
            status_code=status_code,
            headers={
                'Content-Type': 'application/bevyframe'
            }
        )
    else:
        return request.create_response(
            status_code=status_code
        )
