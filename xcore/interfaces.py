from typing import (
    Callable,
    Generic,
    Optional,
    Any,
    Type
)
from .xtypes import T


class AttributeSlot(Generic[T]):
    # TODO - design and implement an attribute interface slot
    ...


class StrategyInterface:
    # TODO - create a interface system that uses FuncSlot and Attribute slots
    ...


class Singleton:
    # TODO - design and implement a singleton
    ...


class FuncSlot(Generic[T]):
    func: Optional[Callable[..., T]]
    alternative_func: Optional[Callable[..., T]]
    is_first_call: bool

    def __init__(self, func: Optional[Callable[..., T]] = None):
        self.func = func  # Initial or default function
        self.alternative_func = None  # Placeholder for an alternative function
        self.is_first_call = True  # To track if the function has been called

    def __call__(self, *args, **kwargs) -> T:
        if self.is_first_call and self.alternative_func:
            self.is_first_call = False
            result = None if self.func is None else self.func(*args, **kwargs)
            if result is None:
                raise ValueError("Function not set.")
            # Swap the function to the alternative after the first call
            self.func = self.alternative_func
            self.alternative_func = None
            return result
        elif self.func:
            return self.func(*args, **kwargs)
        else:
            raise ValueError("Function not set.")

    def setup_lazy_switch(self, func: Callable[..., T]):
        self.alternative_func = func
        return func
    # TODO - design and implement more FuncSlot tools


# Define a type variable for the property type


class xproperty(Generic[T]):
    def __init__(
                self, 
                fget: Optional[Callable[[Any], T]] = None,
                fset: Optional[Callable[[Any, T], None]] = None,
                fdel: Optional[Callable[[Any], None]] = None,
                type_: Optional[Type[T]] = None
            ):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.type = type_
        self.__doc__ = fget.__doc__ if fget is not None else None
        self.__name__ = None  # Placeholder for the attribute name

    def __set_name__(self, owner, name):
        self.__name__ = name

    def __get__(self, obj: Any, objtype: Optional[Type[Any]] = None) -> T:
        # TODO - we need to discard obj type somehow
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj: Any, value: T) -> None:
        if self.fset is None or self.type is None:
            raise AttributeError("can't set attribute")
        if not isinstance(value, self.type):
            raise TypeError(
                f"Expected type {self.type.__name__}, "+
                f"got {type(value).__name__}"
            )
        self.fset(obj, value)

    def __delete__(self, obj: Any) -> None:
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget: Callable[[Any], T]) -> 'xproperty':
        return self.__class__(fget, self.fset, self.fdel, self.type)

    def setter(self, fset: Callable[[Any, T], None]) -> 'xproperty':
        return self.__class__(self.fget, fset, self.fdel, self.type)

    def deleter(self, fdel: Callable[[Any], None]) -> 'xproperty':
        return self.__class__(self.fget, self.fset, fdel, self.type)
    

# Note: The implementation of get, set, and getset class methods may need adjustment.
# Specifically, the use of cls.__name__ inside these methods will not directly yield the property's name.
# This outline serves as a conceptual starting point for the desired functionality.
