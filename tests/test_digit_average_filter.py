import io
import unittest
from unittest.mock import patch

import filters.digit_properties.digit_average_filter as mod


class TestDigitAverageFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_basic(self):
        # Числа: 123 (сред=2), 456 (сред=5), 789 (сред=8)
        # При min_avg=4 должны остаться 456 и 789
        self.assertEqual(mod.apply_filter([123, 456, 789], 4), [456, 789])

    def test_apply_filter_exact_threshold(self):
        # 24 имеет среднее (2+4)/2 = 3.0
        # При min_avg=3.0 число должно быть исключено (avg > min_avg)
        self.assertEqual(mod.apply_filter([24], 3.0), [])
        # При min_avg=2.9 число должно быть включено
        self.assertEqual(mod.apply_filter([24], 2.9), [24])

    def test_apply_filter_single_digit(self):
        # Для однозначных чисел среднее равно самому числу
        self.assertEqual(mod.apply_filter([1, 5, 9], 4), [5, 9])

    def test_apply_filter_with_zero(self):
        # 102 имеет среднее (1+0+2)/3 = 1.0
        self.assertEqual(mod.apply_filter([102], 0.5), [102])
        self.assertEqual(mod.apply_filter([102], 1.5), [])

    def test_apply_filter_negative_numbers(self):
        # Для отрицательных чисел берется abs()
        # -123 -> 123 -> среднее = 2.0
        self.assertEqual(mod.apply_filter([-123, -456], 3), [-456])

    def test_apply_filter_negative_min_avg(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([123], -1)
        self.assertEqual(result, [])
        self.assertIn("минимальное среднее значение не может быть отрицательным", buf.getvalue())

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], 5), [])

    def test_apply_filter_large_numbers(self):
        # 999 имеет среднее 9.0
        # 111 имеет среднее 1.0
        self.assertEqual(mod.apply_filter([999, 111], 5), [999])


if __name__ == "__main__":
    unittest.main()
