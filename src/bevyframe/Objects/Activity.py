class Activity:
    def __init__(self, **kwargs) -> None:
        self.properties = kwargs
        self.context = []

    def add_context(self, item) -> None:
        self.context.append(item)

    def remove_context(self, item) -> None:
        self.context.remove(item)

    def render(self) -> dict:
        d = {"@context": ["https://www.w3.org/ns/activitystreams"] + self.context}
        d.update(self.properties)
        return d
