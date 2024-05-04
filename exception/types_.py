# pylint: skip-file

from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Exception)
NE = TypeVar("NE", bound=Exception)
