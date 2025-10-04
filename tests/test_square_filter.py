import unittest

import filters.math.square_filter as mod


class TestSquareFilter(unittest.TestCase):
    # -------- get_squares_until --------

    def test_get_squares_until_basic(self):
        # Для n=10 должны получить квадраты до и включая ⌊√10⌋ = 3: 1, 4, 9
        expected = {1, 4, 9}
        self.assertEqual(mod.get_squares_until(10), expected)

    def test_get_squares_until_larger_n(self):
        # Для n=25: sqrt(25)=5 -> 1^2, 2^2, 3^2, 4^2, 5^2
        expected = {1, 4, 9, 16, 25}
        self.assertEqual(mod.get_squares_until(25), expected)

    def test_get_squares_until_small_n(self):
        # Для n=2: ⌊√2⌋ = 1 -> {1}
        self.assertEqual(mod.get_squares_until(2), {1})

    # -------- square_filter --------

    def test_square_filter_basic(self):
        # Основной тест из smoke_test
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 4, 9]
        self.assertEqual(mod.square_filter(numbers), expected)

    def test_square_filter_no_squares(self):
        # Список без квадратов
        numbers = [2, 3, 5, 6, 7, 8, 10]
        self.assertEqual(mod.square_filter(numbers), [])

    def test_square_filter_all_squares(self):
        # Список только из квадратов
        numbers = [1, 4, 9, 16, 25]
        self.assertEqual(mod.square_filter(numbers), [1, 4, 9, 16, 25])

    def test_square_filter_single_square(self):
        self.assertEqual(mod.square_filter([4]), [4])

    def test_square_filter_single_non_square(self):
        self.assertEqual(mod.square_filter([5]), [])

    def test_square_filter_with_duplicates(self):
        # Список с повторяющимися числами
        numbers = [1, 1, 4, 4, 5, 9, 9]
        expected = [1, 1, 4, 4, 9, 9]
        self.assertEqual(mod.square_filter(numbers), expected)

    def test_square_filter_large_numbers(self):
        # Большие числа — важно, чтобы квадраты точно определялись
        numbers = [49, 50, 64, 65, 81, 100]
        expected_subset = [49, 64, 81]  # проверяем минимум
        result = mod.square_filter(numbers)
        for x in expected_subset:
            self.assertIn(x, result)

    def test_square_filter_empty_list(self):
        # Пустой список вызовет ошибку в max(numbers)
        with self.assertRaises(ValueError):
            mod.square_filter([])

    def test_square_filter_mixed_order(self):
        # Числа в произвольном порядке
        numbers = [9, 2, 4, 7, 1, 8]
        expected = [9, 4, 1]
        self.assertEqual(mod.square_filter(numbers), expected)


class TestSquareFilterClass(unittest.TestCase):
    # -------- SquareFilter class --------

    def test_class_filter_basic(self):
        filter_obj = mod.SquareFilter()
        numbers = [1, 2, 3, 4, 5]
        expected = [1, 4]
        self.assertEqual(filter_obj.filter(numbers), expected)


if __name__ == "__main__":
    unittest.main()
