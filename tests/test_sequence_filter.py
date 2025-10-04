import io
import unittest
from unittest.mock import patch

import filters.special.sequence_filter as mod


class TestSequenceFilter(unittest.TestCase):
    # -------- _is_in_arith --------

    def test_is_in_arith_basic(self):
        # Арифметическая прогрессия: 2, 5, 8, 11, ... (a1=2, d=3)
        self.assertTrue(mod._is_in_arith(2, 2, 3))   # первый член
        self.assertTrue(mod._is_in_arith(5, 2, 3))   # второй член
        self.assertTrue(mod._is_in_arith(8, 2, 3))   # третий член
        self.assertFalse(mod._is_in_arith(3, 2, 3))  # не в прогрессии

    def test_is_in_arith_zero_step(self):
        # При d=0: все элементы равны a1
        self.assertTrue(mod._is_in_arith(5, 5, 0))
        self.assertFalse(mod._is_in_arith(6, 5, 0))

    def test_is_in_arith_negative_step(self):
        # Убывающая прогрессия: 10, 7, 4, 1, ... (a1=10, d=-3)
        self.assertTrue(mod._is_in_arith(10, 10, -3))
        self.assertTrue(mod._is_in_arith(7, 10, -3))
        self.assertTrue(mod._is_in_arith(1, 10, -3))
        self.assertFalse(mod._is_in_arith(13, 10, -3))  # было бы при n=0

    # -------- _is_power_by_ratio --------

    def test_is_power_by_ratio_basic(self):
        # 8 = 2^3, должно быть True
        self.assertTrue(mod._is_power_by_ratio(8, 2))
        # 9 = 3^2, должно быть True
        self.assertTrue(mod._is_power_by_ratio(9, 3))
        # 1 = r^0 для любого r
        self.assertTrue(mod._is_power_by_ratio(1, 5))

    def test_is_power_by_ratio_edge_cases(self):
        # r = 1: только 1^k = 1
        self.assertTrue(mod._is_power_by_ratio(1, 1))
        self.assertFalse(mod._is_power_by_ratio(2, 1))

        # r = -1: (-1)^k = 1 или -1
        self.assertTrue(mod._is_power_by_ratio(1, -1))
        self.assertTrue(mod._is_power_by_ratio(-1, -1))
        self.assertFalse(mod._is_power_by_ratio(2, -1))

    # -------- _is_in_geom --------

    def test_is_in_geom_basic(self):
        # Геометрическая прогрессия: 2, 6, 18, 54, ... (a1=2, r=3)
        self.assertTrue(mod._is_in_geom(2, 2, 3))   # первый член
        self.assertTrue(mod._is_in_geom(6, 2, 3))   # второй член
        self.assertTrue(mod._is_in_geom(18, 2, 3))  # третий член
        self.assertFalse(mod._is_in_geom(4, 2, 3))  # не в прогрессии

    def test_is_in_geom_zero_cases(self):
        # a1 = 0: прогрессия 0, 0, 0, ...
        self.assertTrue(mod._is_in_geom(0, 0, 5))
        self.assertFalse(mod._is_in_geom(1, 0, 5))

        # r = 0: прогрессия a1, 0, 0, 0, ...
        self.assertTrue(mod._is_in_geom(5, 5, 0))   # первый член
        self.assertTrue(mod._is_in_geom(0, 5, 0))   # остальные члены
        self.assertFalse(mod._is_in_geom(3, 5, 0))

    def test_is_in_geom_ratio_one(self):
        # r = 1: все элементы равны a1
        self.assertTrue(mod._is_in_geom(7, 7, 1))
        self.assertFalse(mod._is_in_geom(8, 7, 1))

    def test_is_in_geom_ratio_minus_one(self):
        # r = -1: a1, -a1, a1, -a1, ...
        self.assertTrue(mod._is_in_geom(5, 5, -1))   # a1
        self.assertTrue(mod._is_in_geom(-5, 5, -1))  # -a1
        self.assertFalse(mod._is_in_geom(3, 5, -1))

    # -------- apply_filter --------

    def test_apply_filter_arithmetic(self):
        # Арифметическая прогрессия: 3, 7, 11, 15, ... (a1=3, d=4)
        numbers = [1, 3, 5, 7, 9, 11, 13, 15]
        params = ("A", 3, 4)
        expected = [3, 7, 11, 15]
        self.assertEqual(mod.apply_filter(numbers, params), expected)

    def test_apply_filter_geometric(self):
        # Геометрическая прогрессия: 2, 4, 8, 16, ... (a1=2, r=2)
        numbers = [1, 2, 3, 4, 6, 8, 12, 16]
        params = ("G", 2, 2)
        expected = [2, 4, 8, 16]
        self.assertEqual(mod.apply_filter(numbers, params), expected)

    def test_apply_filter_invalid_params_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([1, 2, 3], "invalid")
        self.assertEqual(result, [])
        self.assertIn("некорректные параметры фильтра", buf.getvalue())

    def test_apply_filter_invalid_params_length(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([1, 2, 3], ("A", 1))  # не хватает параметра
        self.assertEqual(result, [])
        self.assertIn("некорректные параметры фильтра", buf.getvalue())

    def test_apply_filter_invalid_sequence_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            result = mod.apply_filter([1, 2, 3], ("X", 1, 2))
        self.assertEqual(result, [])
        self.assertIn("тип должен быть 'A' (арифм.) или 'G' (геом.)", buf.getvalue())

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], ("A", 1, 2)), [])

    def test_apply_filter_arithmetic_zero_step(self):
        # d=0: все числа должны равняться a1
        numbers = [1, 5, 5, 7, 5]
        params = ("A", 5, 0)
        expected = [5, 5, 5]
        self.assertEqual(mod.apply_filter(numbers, params), expected)

    def test_apply_filter_geometric_zero_ratio(self):
        # r=0: первый член и нули
        numbers = [0, 3, 5, 7, 0]
        params = ("G", 3, 0)
        expected = [0, 3, 0]
        self.assertEqual(mod.apply_filter(numbers, params), expected)


if __name__ == "__main__":
    unittest.main()
