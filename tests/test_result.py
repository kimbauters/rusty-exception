from unittest import TestCase

from exception import Ok, Err, as_result
from exception import Some, NONE


class TestResult(TestCase):
    def test_equality(self):
        self.assertEqual(Ok("a"), Ok("a"))
        self.assertNotEqual(Ok("a"), Ok("b"))
        self.assertNotEqual(Ok("a"), Ok(2))
        self.assertNotEqual(Ok("0"), Ok(0))
        self.assertNotEqual(Ok("a"), Err(ValueError("some error")))

        error = ValueError("some error")
        self.assertEqual(Err(error), Err(error))
        self.assertNotEqual(Err(ValueError("some error")), Err(ValueError("some error")))
        self.assertNotEqual(Err(ValueError("some error")), Err(ValueError("exception")))
        self.assertNotEqual(Err(ValueError("some error")), Err(TypeError("exception")))
        self.assertNotEqual(Err(ValueError("some error")), Ok("a"))

    def test_repr(self):
        self.assertEqual(repr(Ok("a")), "Ok('a')")
        self.assertEqual(repr(Err(ValueError("some error"))), "Err(ValueError('some error'))")

    def test_is_ok(self):
        self.assertTrue(Ok("a").is_ok())
        self.assertFalse(Err(TypeError()).is_ok())

    def test_is_error(self):
        self.assertFalse(Ok("a").is_err())
        self.assertTrue(Err(TypeError()).is_err())

    def test_ok(self):
        self.assertEqual(Ok("a").ok(), Some("a"))
        self.assertTrue(Err(TypeError()).ok(), NONE)

    def test_err(self):
        self.assertEqual(Ok("a").err(), NONE)
        error = TypeError()
        self.assertTrue(Err(error).err(), Some(error))

    def test_unwrap(self):
        self.assertEqual(Ok("a").unwrap(), "a")
        with self.assertRaises(ValueError):
            Err(ValueError()).unwrap()
        with self.assertRaises(TypeError):
            Err(TypeError()).unwrap()

    def test_unwrap_or(self):
        self.assertEqual(Ok("a").unwrap_or("b"), "a")
        self.assertEqual(Err(ValueError()).unwrap_or("b"), "b")

    def test_unwrap_or_else(self):
        self.assertEqual(Ok("a").unwrap_or_else(lambda _: "b"), "a")
        self.assertEqual(Err(ValueError()).unwrap_or_else(lambda _: "b"), "b")

    def test_expect(self):
        self.assertEqual(Ok("a").expect("expected a"), "a")
        try:
            Err(TypeError()).expect("expected a")
        except ValueError as err:
            self.assertEqual(err.args[0], "expected a")

    def test_map_error(self):
        self.assertEqual(Ok("a").map_error(lambda _: TypeError()).unwrap(), "a")

        with self.assertRaises(NameError):
            Err(TypeError()).map_error(lambda _: NameError()).unwrap()

    def test_is_result(self):
        @as_result()
        def sample_function(data: str) -> int:
            if data == "a":
                return 42
            raise NameError

        self.assertEqual(sample_function("a"), Ok(42))

        with self.assertRaises(NameError):
            sample_function("b").unwrap()

        @as_result(NameError)
        def alt_sample_function(data: str) -> int:
            if data == "a":
                return 42
            if data == "b":
                raise NameError
            raise AttributeError

        self.assertEqual(alt_sample_function("a"), Ok(42))
        with self.assertRaises(NameError):
            alt_sample_function("b").unwrap()

        with self.assertRaises(AttributeError):
            result = alt_sample_function("c")
