import unittest

import filters.math.filter_primes as mod


class TestFilterPrimes(unittest.TestCase):
    # -------- is_prime --------

    def test_is_prime_basic_primes(self):
        # Проверяем основные простые числа
        self.assertTrue(mod.is_prime(2))
        self.assertTrue(mod.is_prime(3))
        self.assertTrue(mod.is_prime(5))
        self.assertTrue(mod.is_prime(7))
        self.assertTrue(mod.is_prime(11))
        self.assertTrue(mod.is_prime(13))

    def test_is_prime_basic_composites(self):
        # Проверяем составные числа
        self.assertFalse(mod.is_prime(4))
        self.assertFalse(mod.is_prime(6))
        self.assertFalse(mod.is_prime(8))
        self.assertFalse(mod.is_prime(9))
        self.assertFalse(mod.is_prime(10))
        self.assertFalse(mod.is_prime(12))

    def test_is_prime_edge_cases(self):
        # Проверяем граничные случаи
        self.assertFalse(mod.is_prime(0))
        self.assertFalse(mod.is_prime(1))
        self.assertFalse(mod.is_prime(-1))
        self.assertFalse(mod.is_prime(-5))

    def test_is_prime_large_prime(self):
        # Проверяем большое простое число
        self.assertTrue(mod.is_prime(97))
        self.assertTrue(mod.is_prime(101))

    def test_is_prime_large_composite(self):
        # Проверяем большое составное число
        self.assertFalse(mod.is_prime(100))  # 100 = 4 * 25
        self.assertFalse(mod.is_prime(99))   # 99 = 9 * 11

    # -------- prime_filter --------

    def test_prime_filter_basic(self):
        # Фильтруем смешанный список
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [2, 3, 5, 7]
        self.assertEqual(mod.prime_filter(numbers), expected)

    def test_prime_filter_no_primes(self):
        # Список без простых чисел
        numbers = [1, 4, 6, 8, 9, 10]
        self.assertEqual(mod.prime_filter(numbers), [])

    def test_prime_filter_all_primes(self):
        # Список только из простых чисел
        numbers = [2, 3, 5, 7, 11]
        self.assertEqual(mod.prime_filter(numbers), [2, 3, 5, 7, 11])

    def test_prime_filter_with_negatives(self):
        # Список с отрицательными числами
        numbers = [-5, -2, 0, 1, 2, 3, 4, 5]
        expected = [2, 3, 5]
        self.assertEqual(mod.prime_filter(numbers), expected)

    def test_prime_filter_empty_list(self):
        self.assertEqual(mod.prime_filter([]), [])

    def test_prime_filter_single_prime(self):
        self.assertEqual(mod.prime_filter([7]), [7])

    def test_prime_filter_single_composite(self):
        self.assertEqual(mod.prime_filter([4]), [])

    def test_prime_filter_with_duplicates(self):
        # Список с повторяющимися числами
        numbers = [2, 2, 3, 3, 4, 5, 5]
        expected = [2, 2, 3, 3, 5, 5]
        self.assertEqual(mod.prime_filter(numbers), expected)


class TestPrimeFilterClass(unittest.TestCase):
    # -------- PrimeFilter class --------

    def test_class_filter_basic(self):
        filter_obj = mod.PrimeFilter()
        numbers = [1, 2, 3, 4, 5]
        expected = [2, 3, 5]
        self.assertEqual(filter_obj.filter(numbers), expected)


if __name__ == "__main__":
    unittest.main()
