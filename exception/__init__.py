# pylint: skip-file

# inspired by # https://jellis18.github.io/post/2021-12-13-python-exceptions-rust-go/
# and the option package for Python: https://github.com/MaT1g3R/option

from .option_ import Option, NONE, Some, as_option
from .result import Err, Ok, Result, as_result

__version__ = "1.0.0"
__all__ = [
    "Option", "NONE", "Some", "as_option",
    "Result", "Ok", "Err", "as_result",
    "__version__"
]
