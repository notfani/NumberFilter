import unittest

import filters.math.power_filter as mod


class TestPowerFilter(unittest.TestCase):
    # -------- is_perfect_power --------

    def test_is_perfect_power_basic_powers(self):
        # Проверяем основные степени
        self.assertTrue(mod.is_perfect_power(4))   # 2^2
        self.assertTrue(mod.is_perfect_power(8))   # 2^3
        self.assertTrue(mod.is_perfect_power(9))   # 3^2
        self.assertTrue(mod.is_perfect_power(16))  # 2^4 или 4^2
        self.assertTrue(mod.is_perfect_power(25))  # 5^2
        self.assertTrue(mod.is_perfect_power(27))  # 3^3

    def test_is_perfect_power_edge_cases(self):
        # Граничные случаи
        self.assertTrue(mod.is_perfect_power(1))   # 1 = любое число в степени 0
        self.assertFalse(mod.is_perfect_power(0))
        self.assertFalse(mod.is_perfect_power(-1))

    def test_is_perfect_power_non_powers(self):
        # Числа, которые не являются степенями
        self.assertFalse(mod.is_perfect_power(2))
        self.assertFalse(mod.is_perfect_power(3))
        self.assertFalse(mod.is_perfect_power(5))
        self.assertFalse(mod.is_perfect_power(6))
        self.assertFalse(mod.is_perfect_power(7))
        self.assertFalse(mod.is_perfect_power(10))

    def test_is_perfect_power_large_numbers(self):
        # Большие числа
        self.assertTrue(mod.is_perfect_power(64))   # 2^6 или 4^3 или 8^2
        self.assertTrue(mod.is_perfect_power(100))  # 10^2
        self.assertTrue(mod.is_perfect_power(125))  # 5^3
        self.assertFalse(mod.is_perfect_power(99))

    # -------- power_filter --------

    def test_power_filter_basic(self):
        # Фильтруем смешанный список
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 4, 8, 9]  # 1=1^n, 4=2^2, 8=2^3, 9=3^2
        self.assertEqual(mod.power_filter(numbers), expected)

    def test_power_filter_no_powers(self):
        # Список без степеней
        numbers = [2, 3, 5, 6, 7, 10]
        self.assertEqual(mod.power_filter(numbers), [])

    def test_power_filter_all_powers(self):
        # Список только из степеней
        numbers = [1, 4, 8, 9, 16, 25]
        self.assertEqual(mod.power_filter(numbers), [1, 4, 8, 9, 16, 25])

    def test_power_filter_with_negatives_and_zero(self):
        # Отрицательные числа и ноль исключаются (x > 0)
        numbers = [-4, -1, 0, 1, 4, 8]
        expected = [1, 4, 8]
        self.assertEqual(mod.power_filter(numbers), expected)

    def test_power_filter_empty_list(self):
        self.assertEqual(mod.power_filter([]), [])

    def test_power_filter_single_power(self):
        self.assertEqual(mod.power_filter([16]), [16])

    def test_power_filter_single_non_power(self):
        self.assertEqual(mod.power_filter([7]), [])

    def test_power_filter_with_duplicates(self):
        # Список с повторяющимися числами
        numbers = [4, 4, 8, 8, 9]
        expected = [4, 4, 8, 8, 9]
        self.assertEqual(mod.power_filter(numbers), expected)

    def test_power_filter_large_powers(self):
        # Большие степени
        numbers = [64, 100, 125, 126, 127, 128]
        expected = [64, 100, 125, 128]  # 64=2^6, 100=10^2, 125=5^3, 128=2^7
        self.assertEqual(mod.power_filter(numbers), expected)


if __name__ == "__main__":
    unittest.main()
