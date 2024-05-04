# pyright: strict
# pylint: disable=unnecessary-pass

"""
This module provides an implementation of the Option type, inspired by Rust's Option type.

The Option type represents an optional value:
  either Some and contains a value, or NONE and does not.
The benefit of an Option over T | None is that it is safe and avoids some of typically
idiomatic code that can lead to issues, e.g. `if value:`.
"""

import functools
from abc import abstractmethod, ABC
from typing import Any, Callable, Generic, NoReturn, ParamSpec

from exception.types_ import T, U

P = ParamSpec("P")


class Option(ABC, Generic[T]):
    """
    The Option type represents an optional value:
      either Some and contains a value, or NONE and does not.
    """
    @abstractmethod
    def is_some(self) -> bool:
        """Returns True if the option is a Some value."""
        pass  # pragma: no cover

    @abstractmethod
    def is_none(self) -> bool:
        """Returns True if the option is a NONE value."""
        pass  # pragma: no cover

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained Some value. Use this method carefully,
        as it will throw a ValueError of it is NONE instead of Some.
        Prefer to use unwrap_or or unwrap_or_else.
        :raise ValueError: If the result is not Some.
        """
        pass  # pragma: no cover

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Returns the contained Some value, or a provided default.
        :param default: The default value to return when not Ok.
        """
        pass  # pragma: no cover

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[], T]) -> T:
        """
        Returns the contained Some value, or computes a default from a closure.
        :param op: The closure with no arguments, expecting a calculation of a default.
        """
        pass  # pragma: no cover

    @abstractmethod
    def map(self, op: Callable[[T], U]) -> "Option[U]":
        """
        Maps the value of Some to a new Option using the given closure,
        or returns NONE if the Option is a NONE value.
        :param op: The closure with no as argument the value if Some, mapped to a new value.
        """
        pass  # pragma: no cover

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained Some value. Raises a ValueError with
        the given `msg` if the value is not Some.
        :param msg: The message to use with ValueError when this result is not Some.
        :raise ValueError: If the result is not Some; will have `msg` as argument.
        """
        pass  # pragma: no cover

    @property
    def value(self) -> T:
        """
        Returns the contained Some value. Raises a ValueError if the value is NONE.
        :raise ValueError: If the result is not Some.
        """
        return self.unwrap()


class _NONE(Option[Any]):
    """Represents a None value."""
    __slots__ = ()

    def __init__(self):
        pass

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, _NONE)

    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def unwrap(self) -> NoReturn:
        raise ValueError("Trying to unwrap a NONE instance.")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[], T]) -> T:
        return op()

    def map(self, op: Callable[[T], U]) -> Option[U]:
        _ = op  # not used
        return NONE

    def expect(self, msg: str) -> NoReturn:
        raise ValueError(msg)

    def __repr__(self) -> str:
        return "None"


NONE: Option[Any] = _NONE()


class Some(Option[T]):
    """Represents a Some value."""
    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Some):
            return self._value == other._value  # type: ignore
        return False

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        _ = default  # not used
        return self._value

    def unwrap_or_else(self, op: Callable[[], T]) -> T:
        _ = op  # not used
        return self.unwrap()

    def map(self, op: Callable[[T], U]) -> Option[U]:
        return Some(op(self.unwrap()))

    def expect(self, msg: str) -> T:
        _ = msg  # not used
        return self._value

    def __repr__(self) -> str:
        return f"Some({repr(self._value)})"


def as_option(func: Callable[P, T | None]) -> Callable[P, Option[T]]:
    """
    Decorator that converts a function returning T | None to a function returning Option[T].
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Option[T]:
        return NONE if (result := func(*args, **kwargs)) is None else Some(result)

    return wrapper
