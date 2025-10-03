import io
import unittest
from unittest.mock import patch

import filters.math.fibonacci_filter as mod


class TestFibonacciFilter(unittest.TestCase):
    # -------- is_perfect_square --------

    def test_is_perfect_square_positive_squares(self):
        self.assertTrue(mod.is_perfect_square(0))
        self.assertTrue(mod.is_perfect_square(1))
        self.assertTrue(mod.is_perfect_square(4))
        self.assertTrue(mod.is_perfect_square(9))
        self.assertTrue(mod.is_perfect_square(16))

    def test_is_perfect_square_non_squares(self):
        self.assertFalse(mod.is_perfect_square(2))
        self.assertFalse(mod.is_perfect_square(3))
        self.assertFalse(mod.is_perfect_square(5))
        self.assertFalse(mod.is_perfect_square(10))

    def test_is_perfect_square_negative_numbers(self):
        self.assertFalse(mod.is_perfect_square(-1))
        self.assertFalse(mod.is_perfect_square(-4))

    # -------- is_fibonacci --------

    def test_is_fibonacci_true(self):
        self.assertTrue(mod.is_fibonacci(0))
        self.assertTrue(mod.is_fibonacci(1))
        self.assertTrue(mod.is_fibonacci(2))
        self.assertTrue(mod.is_fibonacci(3))
        self.assertTrue(mod.is_fibonacci(5))
        self.assertTrue(mod.is_fibonacci(8))
        self.assertTrue(mod.is_fibonacci(13))
        self.assertTrue(mod.is_fibonacci(21))

    def test_is_fibonacci_false(self):
        self.assertFalse(mod.is_fibonacci(4))
        self.assertFalse(mod.is_fibonacci(6))
        self.assertFalse(mod.is_fibonacci(7))
        self.assertFalse(mod.is_fibonacci(9))
        self.assertFalse(mod.is_fibonacci(10))

    # -------- apply_filter --------

    def test_apply_filter_is_fibonacci(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13]
        expected = [0, 1, 2, 3, 5, 8, 13]
        self.assertEqual(mod.apply_filter(numbers, "is_fibonacci"), expected)

    def test_apply_filter_not_fibonacci(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13]
        expected = [4, 6, 7, 9, 10]
        self.assertEqual(mod.apply_filter(numbers, "not_fibonacci"), expected)

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], "is_fibonacci"), [])

    def test_apply_filter_invalid_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 2, 3], "bad_type")
        self.assertEqual(res, [])
        # The original filter does not print an error for invalid type, it just returns empty list.
        # So, no assertIn for error message.

    # -------- get_user_input --------

    def test_get_user_input_is_fibonacci(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "is_fibonacci")

    def test_get_user_input_not_fibonacci(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "not_fibonacci")

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

    def test_run_happy_path_is_fibonacci(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по числам Фибоначчи ===", out)
            self.assertIn("Результат - числа Фибоначчи: [1, 2, 3, 5]", out)

    def test_run_happy_path_not_fibonacci(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по числам Фибоначчи ===", out)
            self.assertIn("Результат - числа, НЕ являющиеся числами Фибоначчи: [4]", out)

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

    def test_run_no_fibonacci_matches(self):
        with patch("builtins.input", side_effect=["4 6 7", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел Фибоначчи", buf.getvalue())

    def test_run_all_fibonacci_matches(self):
        with patch("builtins.input", side_effect=["1 2 3 5", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Все числа являются числами Фибоначчи", buf.getvalue())

    # -------- Класс FibonacciFilter --------

    def test_class_init(self):
        uf = mod.FibonacciFilter()
        self.assertEqual(uf.filter_type, "is_fibonacci")
        uf = mod.FibonacciFilter("not_fibonacci")
        self.assertEqual(uf.filter_type, "not_fibonacci")

    def test_class_set_filter_type_validation(self):
        uf = mod.FibonacciFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'is_fibonacci' или 'not_fibonacci'"):
            uf.set_filter_type("BAD")
        uf.set_filter_type("is_fibonacci")  # валидно

    def test_class_filter_delegates(self):
        uf = mod.FibonacciFilter("is_fibonacci")
        self.assertEqual(uf.filter([1, 2, 3, 4, 5]), [1, 2, 3, 5])
        uf.set_filter_type("not_fibonacci")
        self.assertEqual(uf.filter([1, 2, 3, 4, 5]), [4])

    def test_class_apply_calls_run(self):
        with patch("filters.math.fibonacci_filter.run") as run_mock:
            mod.FibonacciFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
