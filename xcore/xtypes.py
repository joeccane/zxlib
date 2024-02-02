from collections.abc import MutableMapping
from functools import wraps
from typing import (
    Any,
    ClassVar,
    Iterator,
    Tuple,
    Type,
    TypeAlias,
    Callable,
    TypeVar,
    TypeVarTuple,
    Generator,
    Iterable,
    Protocol,
    Generic,
    Annotated,
    AsyncIterable,
    Optional,
    Union
)
from typing_extensions import Self
from dataclasses import dataclass
class EmptyType:
    ...
T = TypeVar('T')
InT = TypeVar('InT')
OutT = TypeVar('OutT')
KeyT = TypeVar('KeyT')
StoreT = TypeVar('StoreT')
FnT = TypeVar('FnT', bound=Callable)
Ts = TypeVarTuple('Ts')

FnGetter: TypeAlias = Callable[[], T]
FnSetter: TypeAlias = Callable[[T], None]
FnGetSet: TypeAlias = Callable[[T|None], T]
FnXForm: TypeAlias = Callable[[InT, *Ts], OutT]
FnProc: TypeAlias = Callable[[T, *Ts], T]
FnExpand: TypeAlias = Callable[[T], Iterable[T]]
FnReduce: TypeAlias = Callable[[Iterable[T]], T]
FnIterate: TypeAlias = Callable[[Iterable[T], *Ts], Generator[T, None, None]]
FnDelegate: TypeAlias = Callable[[*Ts], T]
FnAction: TypeAlias = Callable[[*Ts], None]
FnEvent: TypeAlias = Callable[[*Ts], bool | None]
FnWrapper: TypeAlias = Callable[[FnT, *Ts], FnT]
OptIn: TypeAlias = Optional[Union[T, EmptyType]]
Func: TypeAlias = Callable[..., T]
ConverterT: TypeAlias = FnXForm

null = EmptyType()
def identity(x: T) -> T:
  """This function is a placeholder function for arguments that take a transform function
     it allows a normal default rather than having to check for none.
  """
  return x
def xas_new(x: InT) -> OutT:
    OutT(x)

class Registry(MutableMapping[KeyT, T], Generic[KeyT, T]):
    def __init__(self):
        self.store = dict()

    def __getitem__(self, key: KeyT) -> T:
        return self.store[key]

    def __setitem__(self, key: KeyT, value: T) -> None:
        self.store[key] = value

    def __delitem__(self, key: KeyT) -> None:
        del self.store[key]

    def __iter__(self) -> Iterator[KeyT]:
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def __call__(self, key: KeyT) -> Callable[[T], T]:
        def decorator(value: T) -> T:
            self[key] = value
            return value
        return decorator


class FuncSlot(Generic[T]):
    def __init__(self, func: Optional[Callable[..., T]] = None):
        self.func = func  # Initial or default function
        self.alternative_func = None  # Placeholder for an alternative function
        self.is_first_call = True  # To track if the function has been called

    def __call__(self, *args, **kwargs) -> T:
        if self.is_first_call and self.alternative_func:
            self.is_first_call = False
            result = self.func(*args, **kwargs)
            # Swap the function to the alternative after the first call
            self.func = self.alternative_func
            self.alternative_func = None
            return result
        elif self.func:
            return self.func(*args, **kwargs)
        else:
            raise ValueError("Function not set.")

    def setup_lazy_switch(self, func: Callable[..., T]):
        """Decorator to specify an alternative function to switch to after the first call."""
        self.alternative_func = func
        return func
    # TODO - design and implement more FuncSlot tools
    
class AttributeSlot(Generic[T]):
    # TODO - design and implement an attribute interface slot
    ...

class StrategyInterface:
    # TODO - create a interface system thaqt uses FuncSlot and Attribute slots
    ...


class Singleton:
    # TODO - design and implement a singleton
    ...
    
    
# TODO - Type Aliases for Complex Types: Creating more readable and reusable type aliases for complex data structures.

# TODO - Immutable Data Types: Utility types that ensure objects are immutable once created.