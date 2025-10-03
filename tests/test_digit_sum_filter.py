import io
import unittest
from unittest.mock import patch

import filters.digit_properties.digit_sum_filter as mod


class TestDigitSumFilter(unittest.TestCase):
    # -------- get_digit_sum --------

    def test_get_digit_sum_positive_numbers(self):
        self.assertEqual(mod.get_digit_sum(0), 0)
        self.assertEqual(mod.get_digit_sum(1), 1)
        self.assertEqual(mod.get_digit_sum(9), 9)
        self.assertEqual(mod.get_digit_sum(10), 1)
        self.assertEqual(mod.get_digit_sum(123), 6)
        self.assertEqual(mod.get_digit_sum(999), 27)

    def test_get_digit_sum_negative_numbers(self):
        self.assertEqual(mod.get_digit_sum(-1), 1)
        self.assertEqual(mod.get_digit_sum(-10), 1)
        self.assertEqual(mod.get_digit_sum(-123), 6)

    # -------- apply_filter --------

    def test_apply_filter_equals(self):
        numbers = [1, 10, 12, 21, 100, 123, 99]
        self.assertEqual(mod.apply_filter(numbers, 1, "equals"), [1, 10, 100])
        self.assertEqual(mod.apply_filter(numbers, 3, "equals"), [12, 21])
        self.assertEqual(mod.apply_filter(numbers, 6, "equals"), [123])
        self.assertEqual(mod.apply_filter(numbers, 18, "equals"), [99])

    def test_apply_filter_greater_than(self):
        numbers = [1, 10, 12, 21, 100, 123, 99]
        self.assertEqual(mod.apply_filter(numbers, 5, "greater_than"), [123, 99])
        self.assertEqual(mod.apply_filter(numbers, 10, "greater_than"), [99])
        self.assertEqual(mod.apply_filter(numbers, 0, "greater_than"), [1, 10, 12, 21, 100, 123, 99])

    def test_apply_filter_less_than(self):
        numbers = [1, 10, 12, 21, 100, 123, 99]
        self.assertEqual(mod.apply_filter(numbers, 5, "less_than"), [1, 10, 12, 21, 100])
        self.assertEqual(mod.apply_filter(numbers, 1, "less_than"), [])
        self.assertEqual(mod.apply_filter(numbers, 20, "less_than"), [1, 10, 12, 21, 100, 123, 99])

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], 5, "equals"), [])

    def test_apply_filter_invalid_type(self):
        # The original filter does not print an error for invalid type, it just returns empty list.
        self.assertEqual(mod.apply_filter([1, 2, 3], 1, "bad_type"), [])

    # -------- get_user_input --------

    def test_get_user_input_valid_equals(self):
        with patch("builtins.input", side_effect=["5", "1"]):
            target_sum, filter_type = mod.get_user_input()
            self.assertEqual(target_sum, 5)
            self.assertEqual(filter_type, "equals")

    def test_get_user_input_valid_greater_than(self):
        with patch("builtins.input", side_effect=["5", "2"]):
            target_sum, filter_type = mod.get_user_input()
            self.assertEqual(target_sum, 5)
            self.assertEqual(filter_type, "greater_than")

    def test_get_user_input_valid_less_than(self):
        with patch("builtins.input", side_effect=["5", "3"]):
            target_sum, filter_type = mod.get_user_input()
            self.assertEqual(target_sum, 5)
            self.assertEqual(filter_type, "less_than")

    def test_get_user_input_target_sum_non_integer(self):
        with patch("builtins.input", side_effect=["x", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            target_sum, filter_type = mod.get_user_input()
            self.assertIsNone(target_sum)
            self.assertIsNone(filter_type)
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    def test_get_user_input_filter_type_non_integer(self):
        with patch("builtins.input", side_effect=["5", "x"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            target_sum, filter_type = mod.get_user_input()
            self.assertIsNone(target_sum)
            self.assertIsNone(filter_type)
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    def test_get_user_input_filter_type_wrong_number(self):
        with patch("builtins.input", side_effect=["5", "4"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            target_sum, filter_type = mod.get_user_input()
            self.assertIsNone(target_sum)
            self.assertIsNone(filter_type)
            self.assertIn("Ошибка: выберите 1, 2 или 3", buf.getvalue())

    # -------- run (интерактив) --------

    def test_run_happy_path_equals(self):
        with patch("builtins.input", side_effect=["1 10 12 21", "3", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по сумме цифр ===", out)
            self.assertIn("Результат - числа, сумма цифр которых равна 3: [12, 21]", out)

    def test_run_happy_path_greater_than(self):
        with patch("builtins.input", side_effect=["1 10 12 21", "2", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Результат - числа, сумма цифр которых больше 2: [12, 21]", out)

    def test_run_happy_path_less_than(self):
        with patch("builtins.input", side_effect=["1 10 12 21", "5", "3"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Результат - числа, сумма цифр которых меньше 5: [1, 10, 12, 21]", out)

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x 2", "1", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "1", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: список чисел пуст", buf.getvalue())

    def test_run_no_matches(self):
        with patch("builtins.input", side_effect=["1 2 3", "10", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел, сумма цифр которых равна 10", buf.getvalue())

    def test_run_invalid_target_sum_input(self):
        with patch("builtins.input", side_effect=["1 2 3", "x", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    def test_run_invalid_filter_type_input(self):
        with patch("builtins.input", side_effect=["1 2 3", "5", "x"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    # -------- Класс DigitSumFilter --------

    def test_class_init(self):
        dsf = mod.DigitSumFilter()
        self.assertIsNone(dsf.target_sum)
        self.assertEqual(dsf.filter_type, "equals")
        dsf = mod.DigitSumFilter(target_sum=5, filter_type="greater_than")
        self.assertEqual(dsf.target_sum, 5)
        self.assertEqual(dsf.filter_type, "greater_than")

    def test_class_set_target_sum(self):
        dsf = mod.DigitSumFilter()
        dsf.set_target_sum(10)
        self.assertEqual(dsf.target_sum, 10)

    def test_class_set_filter_type_validation(self):
        dsf = mod.DigitSumFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'equals', 'greater_than' или 'less_than'"):
            dsf.set_filter_type("BAD")
        dsf.set_filter_type("equals")  # валидно

    def test_class_filter_delegates(self):
        dsf = mod.DigitSumFilter(target_sum=3, filter_type="equals")
        self.assertEqual(dsf.filter([1, 10, 12, 21]), [12, 21])
        dsf.set_filter_type("greater_than")
        self.assertEqual(dsf.filter([1, 10, 12, 21]), [])
        dsf.set_target_sum(1)
        self.assertEqual(dsf.filter([1, 10, 12, 21]), [12, 21])

    def test_class_filter_no_target_sum_set(self):
        dsf = mod.DigitSumFilter()
        with self.assertRaisesRegex(ValueError, "Целевая сумма цифр не установлена. Используйте set_target_sum()"):
            dsf.filter([1, 2, 3])

    def test_class_apply_calls_run(self):
        with patch("filters.digit_properties.digit_sum_filter.run") as run_mock:
            mod.DigitSumFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
