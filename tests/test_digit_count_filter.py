import io
import unittest
from unittest.mock import patch

import filters.digit_properties.digit_count_filter as mod


class TestDigitCountFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_positive_numbers(self):
        numbers = [1, 10, 100, 1000, 5, 55, 555]
        self.assertEqual(mod.apply_filter(numbers, 1), [1, 5])
        self.assertEqual(mod.apply_filter(numbers, 2), [10, 55])
        self.assertEqual(mod.apply_filter(numbers, 3), [100, 555])
        self.assertEqual(mod.apply_filter(numbers, 4), [1000])

    def test_apply_filter_negative_numbers(self):
        numbers = [-1, -10, -100, -1000, -5, -55, -555]
        self.assertEqual(mod.apply_filter(numbers, 1), [-1, -5])
        self.assertEqual(mod.apply_filter(numbers, 2), [-10, -55])
        self.assertEqual(mod.apply_filter(numbers, 3), [-100, -555])
        self.assertEqual(mod.apply_filter(numbers, 4), [-1000])

    def test_apply_filter_zero(self):
        numbers = [0]
        self.assertEqual(mod.apply_filter(numbers, 1), [0])
        self.assertEqual(mod.apply_filter(numbers, 2), [])

    def test_apply_filter_mixed_numbers(self):
        numbers = [-10, 0, 1, 100, -555]
        self.assertEqual(mod.apply_filter(numbers, 1), [0, 1])
        self.assertEqual(mod.apply_filter(numbers, 2), [-10])
        self.assertEqual(mod.apply_filter(numbers, 3), [100, -555])

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], 1), [])

    def test_apply_filter_invalid_digit_amount(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 2, 3], 0)
        self.assertEqual(res, [])
        self.assertIn("Ошибка: в числе должен быть как минимум 1 разряд", buf.getvalue())

    # -------- get_user_input --------

    def test_get_user_input_valid(self):
        with patch("builtins.input", return_value="3"):
            self.assertEqual(mod.get_user_input(), 3)

    def test_get_user_input_non_integer(self):
        with patch("builtins.input", return_value="x"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    # -------- run (интерактив) --------

    def test_run_happy_path(self):
        with patch("builtins.input", side_effect=["1 10 100 1000", "3"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по разрядам ===", out)
            self.assertIn("Числа с 3 разрядами: [100]", out)

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

    def test_run_no_matches(self):
        with patch("builtins.input", side_effect=["1 2 3", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел с разрядом 2", buf.getvalue())

    def test_run_invalid_digit_amount_input(self):
        with patch("builtins.input", side_effect=["1 2 3", "0"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: в числе должен быть как минимум 1 разряд", buf.getvalue())

    # -------- Класс DigitCountFilter --------

    def test_class_init(self):
        dcf = mod.DigitCountFilter(2)
        self.assertEqual(dcf.digit_amount, 2)

    def test_class_filter_delegates(self):
        dcf = mod.DigitCountFilter(2)
        self.assertEqual(dcf.filter([1, 10, 100]), [10])

    def test_class_filter_no_digit_amount_set(self):
        dcf = mod.DigitCountFilter(None)
        with self.assertRaisesRegex(ValueError, "Количество разрядов не установлено"):
            dcf.filter([1, 2, 3])

    def test_class_apply_calls_run(self):
        with patch("filters.digit_properties.digit_count_filter.run") as run_mock:
            mod.DigitCountFilter(1).apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
