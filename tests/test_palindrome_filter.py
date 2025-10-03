import io
import unittest
from unittest.mock import patch

import filters.digit_properties.palindrome_filter as mod


class TestPalindromeFilter(unittest.TestCase):
    # -------- is_palindrome --------

    def test_is_palindrome_true(self):
        self.assertTrue(mod.is_palindrome(0))
        self.assertTrue(mod.is_palindrome(1))
        self.assertTrue(mod.is_palindrome(11))
        self.assertTrue(mod.is_palindrome(121))
        self.assertTrue(mod.is_palindrome(1221))
        self.assertTrue(mod.is_palindrome(12321))

    def test_is_palindrome_false(self):
        self.assertFalse(mod.is_palindrome(12))
        self.assertFalse(mod.is_palindrome(123))
        self.assertFalse(mod.is_palindrome(1234))

    def test_is_palindrome_negative_numbers(self):
        self.assertTrue(mod.is_palindrome(-1))
        self.assertTrue(mod.is_palindrome(-11))
        self.assertTrue(mod.is_palindrome(-121))
        self.assertFalse(mod.is_palindrome(-12))

    # -------- apply_filter --------

    def test_apply_filter_is_palindrome(self):
        numbers = [0, 1, 10, 11, 12, 121, 123, -1, -11, -12]
        expected = [0, 1, 11, 121, -1, -11]
        self.assertEqual(mod.apply_filter(numbers, "is_palindrome"), expected)

    def test_apply_filter_not_palindrome(self):
        numbers = [0, 1, 10, 11, 12, 121, 123, -1, -11, -12]
        expected = [10, 12, 123, -12]
        self.assertEqual(mod.apply_filter(numbers, "not_palindrome"), expected)

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], "is_palindrome"), [])

    def test_apply_filter_invalid_type(self):
        # The original filter does not print an error for invalid type, it just returns empty list.
        self.assertEqual(mod.apply_filter([1, 2, 3], "bad_type"), [])

    # -------- get_user_input --------

    def test_get_user_input_is_palindrome(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "is_palindrome")

    def test_get_user_input_not_palindrome(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "not_palindrome")

    def test_get_user_input_wrong_number(self):
        with patch("builtins.input", return_value="3"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("Ошибка: выберите 1 или 2", buf.getvalue())

    def test_get_user_input_non_integer(self):
        with patch("builtins.input", return_value="x"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    # -------- run (интерактив) --------

    def test_run_happy_path_is_palindrome(self):
        with patch("builtins.input", side_effect=["1 10 11 121", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по палиндромам ===", out)
            self.assertIn("Результат - числа-палиндромы: [1, 11, 121]", out)

    def test_run_happy_path_not_palindrome(self):
        with patch("builtins.input", side_effect=["1 10 11 121", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по палиндромам ===", out)
            self.assertIn("Результат - числа, НЕ являющиеся палиндромами: [10]", out)

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x 2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: список чисел пуст", buf.getvalue())

    def test_run_no_palindrome_matches(self):
        with patch("builtins.input", side_effect=["10 20 30", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел-палиндромов", buf.getvalue())

    def test_run_all_palindrome_matches(self):
        with patch("builtins.input", side_effect=["1 11 121", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Все числа являются палиндромами", buf.getvalue())

    # -------- Класс PalindromeFilter --------

    def test_class_init(self):
        pf = mod.PalindromeFilter()
        self.assertEqual(pf.filter_type, "is_palindrome")
        pf = mod.PalindromeFilter("not_palindrome")
        self.assertEqual(pf.filter_type, "not_palindrome")

    def test_class_set_filter_type_validation(self):
        pf = mod.PalindromeFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'is_palindrome' или 'not_palindrome'"):
            pf.set_filter_type("BAD")
        pf.set_filter_type("is_palindrome")  # валидно

    def test_class_filter_delegates(self):
        pf = mod.PalindromeFilter("is_palindrome")
        self.assertEqual(pf.filter([1, 10, 11, 121]), [1, 11, 121])
        pf.set_filter_type("not_palindrome")
        self.assertEqual(pf.filter([1, 10, 11, 121]), [10])

    def test_class_apply_calls_run(self):
        with patch("filters.digit_properties.palindrome_filter.run") as run_mock:
            mod.PalindromeFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
