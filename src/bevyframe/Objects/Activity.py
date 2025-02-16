class Activity:
    def __init__(self, context: list[str] | str | dict) -> None:
        self.properties = {}
        self.context = context if isinstance(context, list) else [context]

    def __call__(self, **kwargs: any) -> None:
        for key, value in kwargs.items():
            self.properties.update({key: value})

    def __setattr__(self, key: str, value: any) -> None:
        self.properties[key] = value

    def __getattr__(self, key: str) -> any:
        if key == 'properties':
            return object.__getattribute__(self, 'properties')
        if key in self.properties:
            return self.properties[key]
        else:
            raise AttributeError

    def pop(self, key: str) -> any:
        return self.properties.pop(key)

    def __delattr__(self, item) -> None:
        self.properties.pop(item)

    def remove_context(self, item: (str, dict)) -> None:
        self.context.remove(item)

    def bf_widget(self) -> dict:
        d = {"@context": ["https://www.w3.org/ns/activitystreams"] + self.context}
        d.update(self.properties)
        return d
