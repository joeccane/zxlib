from typing import Any, Callable, Optional, Generic, cast, Protocol

from .xtypes import Func, Registry, FnAction, FnT


class ixEvent(Protocol):
    def sub(self, callback: FnAction) -> int:
        """Subscribe a callback and return its ID."""
        ...

    def unsub(self, identifier):
        """Unsubscribe a callback by its ID or directly."""
        ...

    def fire(self, *args, **kwargs) -> None:
        """Invoke all subscribed callbacks with given arguments."""
        ...


class xEvent(Generic[FnT]):
    owner: Any
    _callbacks: Registry[int, Func]
    _next_id: int

    def __init__(self, owner: Optional[Any] = None):
        self.owner = owner
        self._callbacks = Registry()
        self._next_id: int = 0

    def sub(self, callback: FnT) -> int:
        callback_id = self._next_id
        self._callbacks[callback_id] = callback
        self._next_id += 1
        return callback_id

    def unsub(self, identifier: FnT | int):
        if callable(identifier):
            id: int = next(
                key for key, value
                in self._callbacks.items()
                if value == identifier
            )
        id = cast(int, identifier)
        self._callbacks.pop(id, None)

    def fire(self, *args, **kwargs) -> None:
        for callback in self._callbacks.values():
            callback(*args, **kwargs)

    def clear(self):
        self._callbacks.clear()

    def __len__(self):
        return len(self._callbacks)

    def __iter__(self):
        return iter(self._callbacks.values())

    def __getitem__(self, identifier):
        if isinstance(identifier, Callable):
            return next(
                value for value in self._callbacks.values()
                if value == identifier
            )
        return self._callbacks[identifier]

    def __delitem__(self, identifier):
        self.unsub(identifier)

    def __set_name__(self, owner, name):
        self.__name__ = name
