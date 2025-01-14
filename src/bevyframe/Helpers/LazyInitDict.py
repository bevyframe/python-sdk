class LazyInitDict:
    def __init__(self, init: callable) -> None:
        self._data: dict = {}
        self._pre_data: dict = {}
        self._initialized = False
        self.init = init
    
    def initialize(self) -> None:
        self.init(self)
        self._pre_data = self._data.copy()
        self._initialized = True

    def is_initialized(self) -> bool:
        return self._initialized

    def is_edited(self) -> bool:
        return self._data != self._pre_data

    def __dict__(self) -> dict:
        if not self._initialized:
            self.initialize()
        return self._data

    def __getitem__(self, key: str) -> any:
        if not self._initialized:
            self.initialize()
        return self._data[key]

    def __setitem__(self, key: str, value: any) -> None:
        if not self._initialized:
            self.initialize()
        self._data[key] = value

    def __repr__(self) -> str:
        if not self._initialized:
            self.initialize()
        return f"LazyInitDict({repr(self._data)})"

    def __str__(self) -> str:
        if not self._initialized:
            self.initialize()
        return str(self._data)

    def __iter__(self) -> iter:
        if not self._initialized:
            self.initialize()
        return iter(self._data)

    def __len__(self) -> int:
        if not self._initialized:
            self.initialize()
        return len(self._data)

    def __contains__(self, item: str) -> bool:
        if not self._initialized:
            self.initialize()
        return item in self._data

    def __delitem__(self, key: str) -> None:
        if not self._initialized:
            self.initialize()
        del self._data[key]

    def __eq__(self, other: any) -> bool:
        if not self._initialized:
            self.initialize()
        return self._data == other

    def __ne__(self, other: any) -> bool:
        if not self._initialized:
            self.initialize()
        return self._data != other

    def __lt__(self, other: any) -> bool:
        if not self._initialized:
            self.initialize()
        return self._data < other

    def __le__(self, other: any) -> bool:
        if not self._initialized:
            self.initialize()
        return self._data <= other

    def __gt__(self, other: any) -> bool:
        if not self._initialized:
            self.initialize()
        return self._data > other

    def __ge__(self, other: any) -> bool:
        if not self._initialized:
            self.initialize()
        return self._data >= other

    def update(self, other: any) -> None:
        if not self._initialized:
            self.initialize()
        self._data.update(other)

    def keys(self) -> any:
        if not self._initialized:
            self.initialize()
        return self._data.keys()

    def values(self) -> iter:
        if not self._initialized:
            self.initialize()
        return self._data.values()

    def items(self) -> iter:
        if not self._initialized:
            self.initialize()
        return self._data.items()

    def get(self, key: str, default=None) -> any:
        if not self._initialized:
            self.initialize()
        return self._data.get(key, default)

    def pop(self, key: str, default=None) -> any:
        if not self._initialized:
            self.initialize()
        return self._data.pop(key, default)

    def popitem(self) -> tuple:
        if not self._initialized:
            self.initialize()
        return self._data.popitem()

    def clear(self) -> None:
        if not self._initialized:
            self.initialize()
        self._data.clear()

    def copy(self) -> dict:
        if not self._initialized:
            self.initialize()
        return self._data.copy()

    def fromkeys(self, seq: iter, value=None) -> dict:
        if not self._initialized:
            self.initialize()
        return self._data.fromkeys(seq, value)

    def setdefault(self, key: str, default=None) -> any:
        if not self._initialized:
            self.initialize()
        return self._data.setdefault(key, default)
