# pyright: strict
# pylint: disable=unnecessary-pass

"""
This module provides an implementation of the Result type, inspired by Rust's Result type.

The Result type represents either success (Ok) or failure (Err).
The benefit of a Result is that it is explicit, must be handled, and cannot cause unexpected
exceptions to be raised (within the limits of the Python language).
"""

import functools
from abc import abstractmethod, ABC
from typing import Any, Callable, Generic, NoReturn, Type, ParamSpec

from exception.option_ import Option, NONE, Some
from exception.types_ import T, E, NE

P = ParamSpec("P")


class Result(ABC, Generic[T, E]):
    """The Result type represents either success (Ok) or failure (Err)."""
    @abstractmethod
    def is_ok(self) -> bool:
        """Returns True if the result is Ok."""
        pass  # pragma: no cover

    @abstractmethod
    def is_err(self) -> bool:
        """Returns True if the result is Err."""
        pass  # pragma: no cover

    @abstractmethod
    def ok(self) -> Option[T]:
        """Converts from Result<T, E> to Option<T>."""
        pass  # pragma: no cover

    @abstractmethod
    def err(self) -> Option[E]:
        """Converts from Result<T, E> to Option<E>."""
        pass  # pragma: no cover

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained Ok value. Use this method carefully,
        as it will throw the underlying exception in Err if it is not an Ok value.
        Prefer to use unwrap_or or unwrap_or_else.
        :raise ValueError: If the result is not Ok.
        """
        pass  # pragma: no cover

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Returns the contained Ok value, or provided default.
        :param default: The default value to return when not Ok.
        """
        pass  # pragma: no cover

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """
        Returns the contained Ok value, or computes a default from a closure.
        :param op: The closure with the Err as argument, expecting a calculation of a default.
        """
        pass  # pragma: no cover

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained Ok value. Raises a ValueError with
        the given `msg` if the value is not Ok.
        :param msg: The message to use with ValueError when this result is not Ok.
        :raise ValueError: If the result is not Ok; will have `msg` as argument.
        """
        pass  # pragma: no cover

    def map_error(self, op: Callable[[Option[E]], NE]) -> "Result[T, NE]":
        """
        Maps a Result<T, E> to Result<T, NE> with a changed error type if
        the result is Err. If the result is Ok then the original type is returned.
        :param op: The closure with the Err as an Option, expecting a new Err type.
        """

        if self.is_err():
            return Err(op(self.err()))
        return self  # type: ignore


class Ok(Result[T, E]):
    """Represents a successful Result."""

    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value  # type: ignore
        return False

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> Option[T]:
        return Some(self._value)

    def err(self) -> Option[E]:
        return NONE

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        _ = default  # not used
        return self.unwrap()

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        _ = op  # not used
        return self.unwrap()

    def expect(self, msg: str) -> T:
        _ = msg  # not used
        return self._value

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"


class Err(Result[T, E]):
    """Represents a failed Result."""

    __slots__ = ("_err",)
    __match_args__ = ("_err",)

    def __init__(self, err: E):
        self._err = err

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Err):
            return self._err == other._err  # type: ignore
        return False

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> Option[T]:
        return NONE

    def err(self) -> Option[E]:
        return Some(self._err)

    def unwrap(self) -> NoReturn:
        raise self._err

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self._err)

    def expect(self, msg: str) -> NoReturn:
        raise ValueError(msg)

    def __repr__(self) -> str:
        return f"Err({repr(self._err)})"


def as_result(
        *exceptions: Type[E],
) -> Callable[[Callable[P, T]], Callable[P, Result[T, E]]]:
    """
    Decorator that converts a function returning T to a function returning Result<T, E>.
    :param exceptions: The exception types to catch and convert to Err. Defaults to Exception.
    """

    if not exceptions:
        exceptions = (Exception,)  # type: ignore

    def decorator(f: Callable[P, T]) -> Callable[P, Result[T, E]]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            try:
                value = f(*args, **kwargs)
                return Ok(value)
            except exceptions as exc:
                return Err(exc)

        return wrapper

    return decorator
