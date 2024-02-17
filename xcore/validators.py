from typing import Callable, Iterable, Protocol, TypeAlias


# Validator protocol
class ixValidator(Protocol):
    def __call__(self, *args, **kwargs) -> bool:
        ...


iValidator: TypeAlias = Callable[..., bool] | ixValidator


# Default no-operation validator
def noop_validator(*args, **kwargs) -> bool:
    return True


def not_none_validator(*args, **kwargs) -> bool:
    for i in args:
        if i is None:
            return False
    for v in kwargs.values():
        if v is None:
            return False
    return True


def one_of_validator(*args, **kwargs) -> bool:
    for i in args:
        if i:
            return True
    for v in kwargs.values():
        if v:
            return True
    return False


def truth_validator(*args, **kwargs) -> bool:
    for i in args:
        if not i:
            return False
    for v in kwargs.values():
        if not v:
            return False
    return True


def type_validator(types):
    def validator(*args, **kwargs) -> bool:
        for i in args:
            if type(i) in types:
                return True
        for v in kwargs.values():
            if type(v) in types:
                return True
        return False
    return validator


def not_type_validator(types):
    def validator(*args, **kwargs) -> bool:
        for i in args:
            if type(i) not in types:
                return True
        for v in kwargs.values():
            if type(v) not in types:
                return True
        return False
    return validator


def predicate_validator(
            getter: Callable[..., Iterable],
            predicate: Callable[..., bool]
        ) -> iValidator:
    def validator(*args, **kwargs) -> bool:
        for i in getter(*args, **kwargs):
            if not predicate(i):
                return False
        return True
    return validator
