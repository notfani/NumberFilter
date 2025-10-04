import io
import unittest
from unittest.mock import patch

import filters.digit_properties.digit_delta_filter as mod


class TestDigitDeltaFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_basic(self):
        # Текущая логика использует сумму первой и последней цифры
        # 123: первая=1, последняя=3, сумма=4
        # 456: первая=4, последняя=6, сумма=10
        # При threshold=5, остается только 456 (10 > 5)
        self.assertEqual(mod.apply_filter([123, 456], 5), [456])

    def test_apply_filter_single_digit(self):
        # Для однозначного числа первая и последняя цифры одинаковы
        # 5: первая=5, последняя=5, сумма=10
        self.assertEqual(mod.apply_filter([5], 8), [5])
        self.assertEqual(mod.apply_filter([5], 12), [])

    def test_apply_filter_threshold_boundary(self):
        # 19: первая=1, последняя=9, сумма=10
        self.assertEqual(mod.apply_filter([19], 10), [])  # 10 не больше 10
        self.assertEqual(mod.apply_filter([19], 9), [19])  # 10 больше 9

    def test_apply_filter_negative_numbers(self):
        # Для отрицательных чисел берется abs()
        # -123 -> 123: первая=1, последняя=3, сумма=4
        self.assertEqual(mod.apply_filter([-123], 3), [-123])

    def test_apply_filter_invalid_threshold_negative(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([123], -1)
        self.assertEqual(result, [])
        self.assertIn("порог должен быть целым числом в диапазоне 0–9", buf.getvalue())

    def test_apply_filter_invalid_threshold_too_large(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([123], 10)
        self.assertEqual(result, [])
        self.assertIn("порог должен быть целым числом в диапазоне 0–9", buf.getvalue())

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], 5), [])

    def test_apply_filter_zero_threshold(self):
        # При threshold=0 должны проходить числа с суммой > 0
        # 10: первая=1, последняя=0, сумма=1 > 0
        self.assertEqual(mod.apply_filter([10], 0), [10])


if __name__ == "__main__":
    unittest.main()
