from collections.abc import MutableMapping
from typing import (
    AsyncIterable,
    Iterator,
    TypeAlias,
    Callable,
    TypeVar,
    TypeVarTuple,
    Generator,
    Iterable,
    Generic,
    Optional,
    Union,
    Awaitable,
    AsyncGenerator,
    AsyncContextManager
)

class EmptyType:
    ...

T = TypeVar('T')
InT = TypeVar('InT')
OutT = TypeVar('OutT')
_OutT = TypeVar('_OutT')
KeyT = TypeVar('KeyT')
StoreT = TypeVar('StoreT')
FnT = TypeVar('FnT', bound=Callable)
Ts = TypeVarTuple('Ts')

FnGetter: TypeAlias = Callable[[], T]
'''A function that returns a value of type `T`.'''

FnSetter: TypeAlias = Callable[[T], None]
'''A function that sets a value of type `T`.'''

FnGetSet: TypeAlias = Callable[[Optional[T]], T]
'''A function that may get or set a value of type `T`, depending on whether an argument is provided.'''

FnXForm: TypeAlias = Callable[[InT, *Ts], OutT]  # type: ignore
'''A transformation function from `InT` to `OutT`, potentially using additional arguments `Ts`.'''

FnProc: TypeAlias = Callable[[T, *Ts], T]  # type: ignore
'''A processing function that takes an input of type `T`, processes it with additional arguments `Ts`, and returns a result of type `T`.'''

FnExpand: TypeAlias = Callable[[T], Iterable[T]]
'''A function that expands a single input of type `T` into an iterable of `T`.'''

FnReduce: TypeAlias = Callable[[Iterable[T]], T]
'''A function that reduces an iterable of `T` to a single value of type `T`.'''

FnIterate: TypeAlias = Callable[[Iterable[T], *Ts], Generator[T, None, None]]  # type: ignore
'''A function that iterates over an iterable of `T`, potentially processing each item with additional arguments `Ts`, yielding results of type `T`.'''

FnDelegate: TypeAlias = Callable[[Ts], T]  # type: ignore
'''A delegate function that takes arguments `Ts` and returns a result of type `T`.'''

FnAction: TypeAlias = Callable[[Ts], None]  # type: ignore
'''An action function that performs an operation using arguments `Ts`, without returning a result.'''

FnEvent: TypeAlias = Callable[[Ts], bool | None]  # type: ignore
'''An event function that takes arguments `Ts` and returns a boolean or None, indicating the outcome of an event.'''

FnWrapper: TypeAlias = Callable[[FnT, Ts], FnT]  # type: ignore
'''A wrapper function that takes a function `FnT` and additional arguments `Ts`, returning a potentially modified version of `FnT`.'''

OptIn: TypeAlias = Optional[Union[T, EmptyType]]
'''An optional input that can be either of type `T`, `EmptyType`, or `None`.'''

Func: TypeAlias = Callable[..., T]
'''A generic function type that takes any arguments and returns a result of type `T`.'''

# Asynchronous type aliases
AsyncFunc: TypeAlias = Callable[..., Awaitable[T]]
'''An asynchronous function type that takes any arguments and returns an awaitable result of type `T`.'''

AsyncCallback: TypeAlias = Callable[..., Awaitable[None]]
'''An asynchronous callback function that takes any arguments, performs an operation, and returns an awaitable `None`.'''

AsyncFactory: TypeAlias = Callable[..., Awaitable[T]]
'''An asynchronous factory function that takes any arguments and returns an awaitable result of type `T`.'''

AsyncIterableT: TypeAlias = AsyncIterable[T]
'''An asynchronous iterable type over elements of type `T`.'''

AsyncContextManagerT: TypeAlias = Callable[..., Awaitable[AsyncContextManager[T]]]
'''An asynchronous context manager type that takes any arguments and returns an awaitable `AsyncContextManager` of type `T`.'''

AsyncPredicate: TypeAlias = Callable[..., Awaitable[bool]]
'''An asynchronous predicate function that takes any arguments, evaluates a condition, and returns an awaitable boolean result.'''

AsyncReducer: TypeAlias = Callable[[Iterable[T], Ts], Awaitable[T]]  # type: ignore
'''An asynchronous reducer function that takes an iterable of `T` and additional arguments `Ts`, and returns an awaitable result of type `T`.'''

AsyncBiDirectionalXForm: TypeAlias = Callable[[Union[InT, OutT], Ts], Awaitable[Union[OutT, InT]]]  # type: ignore
'''An asynchronous bidirectional transformation function that can convert between `InT` and `OutT` using additional arguments `Ts`, returning an awaitable result.'''

# Asynchronous functional types
AsyncFnXForm: TypeAlias = Callable[[InT, Ts], Awaitable[OutT]]  # type: ignore
'''An asynchronous function that transforms an input of type `InT` into an awaitable result of type `OutT`, using additional arguments `Ts`.'''

AsyncFnProc: TypeAlias = Callable[[T, Ts], Awaitable[T]]  # type: ignore
'''An asynchronous processing function that takes an input of type `T`, processes it with additional arguments `Ts`, and returns an awaitable result of type `T`.'''

AsyncFnIterate: TypeAlias = Callable[[Iterable[T], Ts], AsyncGenerator[T, None]]  # type: ignore
'''An asynchronous iteration function that processes each item of an iterable of `T` with additional arguments `Ts`, yielding awaitable results of type `T`.'''

AsyncFnDelegate: TypeAlias = Callable[[Ts], Awaitable[T]]  # type: ignore
'''An asynchronous delegate function that takes arguments `Ts` and returns an awaitable result of type `T`.'''

AsyncFnAction: TypeAlias = Callable[[Ts], Awaitable[None]]  # type: ignore
'''An asynchronous action function that performs an operation using arguments `Ts`, returning an awaitable `None`.'''

AsyncFnEvent: TypeAlias = Callable[[Ts], Awaitable[bool | None]]  # type: ignore
'''An asynchronous event function that takes arguments `Ts` and returns an awaitable boolean or None, indicating the outcome of an event.'''


null = EmptyType()

def identity(x: T) -> T:
    return x

def xas_new(x: InT) -> OutT:  # type: ignore
    return OutT(x)  # type: ignore

class Registry(MutableMapping[KeyT, T], Generic[KeyT, T]):
    def __init__(self):
        self.store = dict()

    def __getitem__(self, key: KeyT) -> T:
        # This method will raise KeyError if the key is not found, which is standard Python behavior.
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

    def __repr__(self) -> str:
        """Return the string representation of the registry."""
        return f"{self.__class__.__name__}({self.store})"

reg = Registry[str, str]()
