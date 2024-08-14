"""Exceptions for BevyFrame"""


class WidgetContentEmptyError(Exception):
    """Raised when a widget content is empty"""
    pass


class Error404(Exception):
    """Raised when a page is not found"""
    pass
