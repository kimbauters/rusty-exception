# Rust-y Exception

This package provides implementations of the `Option` and `Result` types in Python, inspired by Rust's `Option` and `Result` types. These types offer a safer and more explicit way to handle optional values and error handling compared to using `None` or raising exceptions directly.

## Option
The `Option` type represents an optional value: either `Some` (containing a value) or `NONE` (not containing a value). It provides a way to avoid some of the idiomatic code that can lead to issues, such as using `if value:` to check for the presence of a value.

### Example Usage
```python
from exception import Some, NONE, as_option

@as_option  # trivially convert (existing) code to Option<str>
def get_value(key: str) -> str | None:
    # Some logic to retrieve a value or return None
    ...

result = get_value("key")
if result.is_some():
    value = result.unwrap()
    print(f"Value: {value}")
else:
    print("No value found")

default_value = result.unwrap_or("default")
print(f"Value or default: {default_value}")
```

## Result
The Result type represents either success (`Ok`) or failure (`Err`). It provides a way to handle errors and exceptions explicitly, ensuring that they are handled and cannot cause unexpected exceptions to be raised (within the limits of the Python language).

### Example Usage
```python
from exception import Ok, Err, as_result

@as_result(ValueError)  # convert code to Result<float, ValueError>
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

result = divide(10, 2)
if result.is_ok():
    value = result.unwrap()
    print(f"Result: {value}")
else:
    error = result.err().unwrap()
    print(f"Error: {error}")

default_value = result.unwrap_or(0)
print(f"Result or default: {default_value}")

# alternatively, to capture *any* exception simply use @as_result()
# to capture many exception types use @as_result(ValueError, TypeError)
```

## Installation
To use the `Option` and `Result` types in your Python project, simply copy the `exception` module into your project directory. Alternatively, install directly from GitHub using `pip`:
```
pip install git+https://github.com/kimbauters/rusty-exception.git
```
*The package is not uploaded to PyPi and there are no plans to do so.* This package has no requirements, but does rely on modern Python versions (3.10+) and does not do any attempt to support older versions. 

## Testing
The project includes unit tests for both the `Option` and `Result` types. To run the tests, execute the following command:
```
python -m unittest discover tests
```

## Contributing
Contributions to this project are welcome, as long as you submit pull requests on the project's GitHub repository. This package targets Python 3.10+. All pull requests should fully pass Pylint and Pyright (strict) checks. Any pull request should have full Pytest code coverage (as in sensibly full coverage, not 100% for the sake of it).

## License
This project is licensed under the MIT License. Do with it what you want. Don't blame me for anything.