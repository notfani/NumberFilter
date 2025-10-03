import io
import unittest
from unittest.mock import patch

import filters.basic.range_filter as mod


class TestRangeFilter(unittest.TestCase):
    # ---- apply_filter ----

    def test_apply_filter_inclusive_bounds(self):
        # Должно быть ВКЛЮЧИТЕЛЬНО: [2,4] -> 2,3,4
        res = mod.apply_filter([1, 2, 3, 4, 5], 2, 4)
        self.assertEqual(res, [2, 3, 4])

    def test_apply_filter_min_greater_than_max_prints_and_returns_empty(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 2, 3], 10, 5)
        self.assertEqual(res, [])
        self.assertIn("минимальное значение не может быть больше максимального", buf.getvalue())

    def test_apply_filter_negative_numbers(self):
        # Проверяем работу с отрицательными
        res = mod.apply_filter([-10, -7, -1, 0, 3, 8], -7, 3)
        self.assertEqual(res, [-7, -1, 0, 3])

    def test_apply_filter_empty_input_list(self):
        self.assertEqual(mod.apply_filter([], 0, 100), [])

    # ---- get_user_input ----

    def test_get_user_input_valid(self):
        # Ввод: мин, макс
        with patch("builtins.input", side_effect=["-5", "12"]):
            self.assertEqual(mod.get_user_input(), (-5, 12))

    def test_get_user_input_invalid_min(self):
        with patch("builtins.input", side_effect=["abc"]):
            with patch("sys.stdout", new_callable=io.StringIO) as buf:
                self.assertIsNone(mod.get_user_input())
                self.assertIn("введите целое число", buf.getvalue())

    def test_get_user_input_invalid_max(self):
        with patch("builtins.input", side_effect=["1", "x"]):
            with patch("sys.stdout", new_callable=io.StringIO) as buf:
                self.assertIsNone(mod.get_user_input())
                self.assertIn("введите целое число", buf.getvalue())

    # ---- run() интерактив ----

    def test_run_happy_path(self):
        # Числа -> мин -> макс
        with patch("builtins.input", side_effect=["1 2 3 4 5", "2", "4"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Фильтр по диапазону", out)
            self.assertIn("Числа в диапазоне от 2 до 4: [2, 3, 4]", out)

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x 3", "0", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "0", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("список чисел пуст", buf.getvalue())

    def test_run_no_numbers_in_range(self):
        with patch("builtins.input", side_effect=["1 2 3", "10", "20"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел в диапазоне от 10 до 20", buf.getvalue())

    # ---- Класс RangeFilter ----

    def test_class_filter_requires_set_range(self):
        rf = mod.RangeFilter()
        with self.assertRaisesRegex(ValueError, "Диапазон не установлен"):
            rf.filter([1, 2, 3])

    def test_class_set_range_rejects_inverted_bounds(self):
        rf = mod.RangeFilter()
        with self.assertRaisesRegex(ValueError, "Минимальное значение не может быть больше максимального"):
            rf.set_range(5, 1)

    def test_class_filter_delegates_to_apply_filter(self):
        rf = mod.RangeFilter(2, 4)
        self.assertEqual(rf.filter([1, 2, 3, 4, 5]), [2, 3, 4])

    def test_class_apply_calls_run(self):
        with patch("filters.basic.range_filter.run") as run_mock:
            mod.RangeFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
