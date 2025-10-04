import io
import unittest
from unittest.mock import patch

import filters.digit_properties.digit_difference_filter as mod


class TestDigitDifferenceFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_basic(self):
        # 123: max=3, min=1, разность=2
        # 159: max=9, min=1, разность=8
        # При min_limit=5 остается только 159
        self.assertEqual(mod.apply_filter([123, 159], 5), [159])

    def test_apply_filter_same_digits(self):
        # 111: max=1, min=1, разность=0
        # При любом min_limit >= 1 такие числа исключаются
        self.assertEqual(mod.apply_filter([111, 222], 1), [])

    def test_apply_filter_single_digit(self):
        # 5: max=5, min=5, разность=0
        self.assertEqual(mod.apply_filter([5], 1), [])

    def test_apply_filter_exact_threshold(self):
        # 135: max=5, min=1, разность=4
        self.assertEqual(mod.apply_filter([135], 4), [135])  # 4 >= 4
        self.assertEqual(mod.apply_filter([135], 5), [])    # 4 < 5

    def test_apply_filter_negative_numbers(self):
        # -190: abs() -> 190, max=9, min=0, разность=9
        self.assertEqual(mod.apply_filter([-190], 8), [-190])

    def test_apply_filter_with_zero(self):
        # 102: max=2, min=0, разность=2
        self.assertEqual(mod.apply_filter([102], 2), [102])
        self.assertEqual(mod.apply_filter([102], 3), [])

    def test_apply_filter_invalid_limit_zero(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([123], 0)
        self.assertEqual(result, [])
        self.assertIn("порог должен быть как минимум 1", buf.getvalue())

    def test_apply_filter_invalid_limit_negative(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([123], -1)
        self.assertEqual(result, [])
        self.assertIn("порог должен быть как минимум 1", buf.getvalue())

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], 3), [])

    def test_apply_filter_large_difference(self):
        # 901: max=9, min=0, разность=9
        self.assertEqual(mod.apply_filter([901], 9), [901])


if __name__ == "__main__":
    unittest.main()
