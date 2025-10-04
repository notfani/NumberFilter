import io
import unittest
from unittest.mock import patch

import filters.digit_properties.digit_delta_filter as mod


class TestDigitDeltaFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_basic(self):
        # Логика использует разность между первой и последней цифрой
        # 123: первая=1, последняя=3, разность=|1-3|=2
        # 456: первая=4, последняя=6, разность=|4-6|=2
        # При threshold=1, остаются оба числа (2 > 1)
        self.assertEqual(mod.apply_filter([123, 456], 1), [123, 456])

        # При threshold=3, не остается ни одного (2 не больше 3)
        self.assertEqual(mod.apply_filter([123, 456], 3), [])

    def test_apply_filter_single_digit(self):
        # Для однозначного числа первая и последняя цифры одинаковы
        # 5: первая=5, последняя=5, разность=|5-5|=0
        self.assertEqual(mod.apply_filter([5], 0), [])  # 0 не больше 0
        self.assertEqual(mod.apply_filter([5], 1), [])  # 0 не больше 1

    def test_apply_filter_threshold_boundary(self):
        # 19: первая=1, последняя=9, разность=|1-9|=8
        self.assertEqual(mod.apply_filter([19], 8), [])  # 8 не больше 8
        self.assertEqual(mod.apply_filter([19], 7), [19])  # 8 больше 7

    def test_apply_filter_negative_numbers(self):
        # Для отрицательных чисел берется abs()
        # -123 -> 123: первая=1, последняя=3, разность=|1-3|=2
        self.assertEqual(mod.apply_filter([-123], 1), [-123])

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
        # При threshold=0 должны проходить числа с разностью > 0
        # 10: первая=1, последняя=0, разность=|1-0|=1 > 0
        self.assertEqual(mod.apply_filter([10], 0), [10])

        # 11: первая=1, последняя=1, разность=|1-1|=0 не больше 0
        self.assertEqual(mod.apply_filter([11], 0), [])


if __name__ == "__main__":
    unittest.main()
