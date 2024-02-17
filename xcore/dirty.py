from typing import Callable, Any, Dict, List, Protocol


class Notifier:
    _notifiers: Dict[Callable[..., Any], List[Callable[..., Any]]] = {}

    @classmethod
    def notifier(cls, func: Callable[..., Any]) -> Callable[..., Any]:
        def decorator(notify_func: Callable[..., Any]) -> Callable[..., Any]:
            if func not in cls._notifiers:
                cls._notifiers[func] = []
            cls._notifiers[func].append(notify_func)
            return notify_func
        return decorator

    @classmethod
    def notify(
                cls, func: Callable[..., Any], *args: Any, **kwargs: Any
            ) -> None:
        for notify_func in cls._notifiers.get(func, []):
            notify_func(*args, **kwargs)


class iDirty(Protocol):
    @property
    def is_dirty(self) -> bool:
        ...

    def set_dirty(self) -> None:
        ...

    def reset(self) -> None:
        ...


class Dirty(iDirty):
    _is_dirty: bool

    def __init__(self) -> None:
        self._is_dirty = False

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def set_dirty(self) -> None:
        self._is_dirty = True
        Notifier.notify(Dirty.set_dirty, self)

    def reset(self) -> None:
        self._is_dirty = False
        Notifier.notify(Dirty.reset, self)


# Usage Example
@Notifier.notifier(Dirty.set_dirty)
def on_set_dirty(instance: Dirty) -> None:
    print(f"{instance} is dirty")


@Notifier.notifier(Dirty.reset)
def on_reset(instance: Dirty) -> None:
    print(f"{instance} has been reset")


dirty_instance = Dirty()
dirty_instance.set_dirty()  # Triggers the static notifier
dirty_instance.reset()      # Triggers the static notifier
