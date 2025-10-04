import unittest

import filters.math.divisor_count_filter as mod


class TestDivisorCountFilter(unittest.TestCase):
    # -------- divisor_count --------

    def test_divisor_count_basic(self):
        # 12 имеет делители: 1, 2, 3, 4, 6, 12 (всего 6)
        self.assertEqual(mod.divisor_count(12), 6)

    def test_divisor_count_prime(self):
        # У простых чисел ровно 2 делителя
        self.assertEqual(mod.divisor_count(7), 2)
        self.assertEqual(mod.divisor_count(13), 2)

    def test_divisor_count_perfect_square(self):
        # 16 = 4^2, делители: 1, 2, 4, 8, 16 (всего 5)
        self.assertEqual(mod.divisor_count(16), 5)

    def test_divisor_count_one(self):
        # У 1 только один делитель - само число
        self.assertEqual(mod.divisor_count(1), 1)

    def test_divisor_count_zero(self):
        # Для 0 возвращается 0
        self.assertEqual(mod.divisor_count(0), 0)

    def test_divisor_count_negative(self):
        # Для отрицательных чисел берется abs()
        self.assertEqual(mod.divisor_count(-12), 6)

    # -------- divisor_count_filter --------

    def test_divisor_count_filter_equals(self):
        # Ищем числа с ровно 4 делителями
        # 6 имеет делители: 1, 2, 3, 6 (4 делителя)
        # 8 имеет делители: 1, 2, 4, 8 (4 делителя)
        # 12 имеет 6 делителей
        self.assertEqual(mod.divisor_count_filter([6, 8, 12], 4, "equals"), [6, 8])

    def test_divisor_count_filter_greater(self):
        # Ищем числа с количеством делителей больше 4
        # 12 имеет 6 делителей > 4
        self.assertEqual(mod.divisor_count_filter([6, 8, 12], 4, "greater"), [12])

    def test_divisor_count_filter_less(self):
        # Ищем числа с количеством делителей меньше 4
        # 7 (простое) имеет 2 делителя < 4
        self.assertEqual(mod.divisor_count_filter([6, 7, 12], 4, "less"), [7])

    def test_divisor_count_filter_invalid_target_zero(self):
        # target <= 0 должен возвращать пустой список
        self.assertEqual(mod.divisor_count_filter([6, 8], 0, "equals"), [])

    def test_divisor_count_filter_invalid_target_negative(self):
        self.assertEqual(mod.divisor_count_filter([6, 8], -1, "equals"), [])

    def test_divisor_count_filter_invalid_mode(self):
        # Неверный режим должен возвращать пустой список
        self.assertEqual(mod.divisor_count_filter([6, 8], 4, "invalid"), [])

    def test_divisor_count_filter_empty_list(self):
        self.assertEqual(mod.divisor_count_filter([], 4, "equals"), [])

    def test_divisor_count_filter_negative_numbers(self):
        # Для отрицательных чисел используется abs()
        self.assertEqual(mod.divisor_count_filter([-6, -8], 4, "equals"), [-6, -8])


if __name__ == "__main__":
    unittest.main()
