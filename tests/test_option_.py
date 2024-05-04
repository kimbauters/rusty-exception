from unittest import TestCase

from exception import Some, NONE, as_option


class TestOption(TestCase):
    def test_equality(self):
        self.assertEqual(Some("a"), Some("a"))
        self.assertNotEqual(Some("a"), Some("b"))
        self.assertNotEqual(Some("a"), Some(2))
        self.assertNotEqual(Some("0"), Some(0))
        self.assertNotEqual(Some("a"), NONE)
        self.assertEqual(NONE, NONE)

    def test_repr(self):
        self.assertEqual(repr(Some("a")), "Some('a')")
        self.assertEqual(repr(NONE), "None")

    def test_is_some(self):
        self.assertTrue(Some("some").is_some())
        self.assertFalse(NONE.is_some())

    def test_is_none(self):
        self.assertFalse(Some("some").is_none())
        self.assertTrue(NONE.is_none())

    def test_unwrap(self):
        self.assertEqual(Some("some").unwrap(), "some")
        with self.assertRaises(ValueError):
            NONE.unwrap()

    def test_unwrap_or(self):
        self.assertEqual(Some("some").unwrap_or("other"), "some")
        self.assertEqual(NONE.unwrap_or("other"), "other")

    def test_unwrap_or_else(self):
        self.assertEqual(Some("some").unwrap_or_else(lambda: "other"), "some")
        self.assertEqual(NONE.unwrap_or_else(lambda: "other"), "other")

    def test_map(self):
        self.assertEqual(Some(5).map(lambda x: x + 1), Some(6))
        self.assertEqual(NONE.map(lambda x: x + 1), NONE)

    def test_expect(self):
        self.assertEqual(Some("some").expect("other error"), "some")
        try:
            self.assertEqual(NONE.expect("other error"), "some")
        except ValueError as err:
            self.assertEqual(err.args[0], "other error")

    def test_value(self):
        self.assertEqual(Some("some").value, "some")
        with self.assertRaises(ValueError):
            NONE.unwrap()

    def test_match(self):
        value = Some("some")
        match value:
            case Some(v): self.assertEqual(v, "some")
            case _: self.fail()

    def test_is_option(self):
        @as_option
        def sample_function(data: str) -> int | None:
            return 42 if data == "a" else None

        self.assertEqual(sample_function("a"), Some(42))
        self.assertEqual(sample_function("b"), NONE)
