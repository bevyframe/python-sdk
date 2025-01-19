from bevyframe import Button


class CustomButton(Button):
    def __init__(self, selector='', **kwargs) -> None:
        super().__init__(selector, **kwargs)
