import io
import unittest
from unittest.mock import patch

import filters.math.semiprime_filter as mod


class TestSemiprimeFilter(unittest.TestCase):
    # -------- is_prime --------

    def test_is_prime_true(self):
        self.assertFalse(mod.is_prime(0))
        self.assertFalse(mod.is_prime(1))
        self.assertTrue(mod.is_prime(2))
        self.assertTrue(mod.is_prime(3))
        self.assertFalse(mod.is_prime(4))
        self.assertTrue(mod.is_prime(5))
        self.assertTrue(mod.is_prime(7))
        self.assertTrue(mod.is_prime(11))
        self.assertTrue(mod.is_prime(13))

    def test_is_prime_false(self):
        self.assertFalse(mod.is_prime(6))
        self.assertFalse(mod.is_prime(8))
        self.assertFalse(mod.is_prime(9))
        self.assertFalse(mod.is_prime(10))
        self.assertFalse(mod.is_prime(15))

    # -------- is_semiprime --------

    def test_is_semiprime_true(self):
        self.assertTrue(mod.is_semiprime(4))  # 2*2
        self.assertTrue(mod.is_semiprime(6))  # 2*3
        self.assertTrue(mod.is_semiprime(9))  # 3*3
        self.assertTrue(mod.is_semiprime(10)) # 2*5
        self.assertTrue(mod.is_semiprime(14)) # 2*7
        self.assertTrue(mod.is_semiprime(15)) # 3*5
        self.assertTrue(mod.is_semiprime(21)) # 3*7
        self.assertTrue(mod.is_semiprime(22)) # 2*11
        self.assertTrue(mod.is_semiprime(25)) # 5*5

    def test_is_semiprime_false(self):
        self.assertFalse(mod.is_semiprime(0))
        self.assertFalse(mod.is_semiprime(1))
        self.assertFalse(mod.is_semiprime(2))
        self.assertFalse(mod.is_semiprime(3))
        self.assertFalse(mod.is_semiprime(5))  # Prime
        self.assertFalse(mod.is_semiprime(7))  # Prime
        self.assertFalse(mod.is_semiprime(8))  # 2*2*2
        self.assertFalse(mod.is_semiprime(12)) # 2*2*3
        self.assertFalse(mod.is_semiprime(18)) # 2*3*3
        self.assertFalse(mod.is_semiprime(24)) # 2*2*2*3
        self.assertFalse(mod.is_semiprime(27)) # 3*3*3

    # -------- apply_filter --------

    def test_apply_filter_is_semiprime(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        expected = [4, 6, 9, 10, 14, 15]
        self.assertEqual(mod.apply_filter(numbers, "is_semiprime"), expected)

    def test_apply_filter_not_semiprime(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        expected = [0, 1, 2, 3, 5, 7, 8, 11, 12, 13]
        self.assertEqual(mod.apply_filter(numbers, "not_semiprime"), expected)

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([], "is_semiprime"), [])

    # -------- get_user_input --------

    def test_get_user_input_is_semiprime(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "is_semiprime")

    def test_get_user_input_not_semiprime(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "not_semiprime")

    def test_get_user_input_wrong_number(self):
        with patch("builtins.input", return_value="3"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("Ошибка: выберите 1 или 2", buf.getvalue())

    def test_get_user_input_non_integer(self):
        with patch("builtins.input", return_value="x"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("Ошибка: введите целое число", buf.getvalue())

    # -------- run (интерактив) --------

    def test_run_happy_path_is_semiprime(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5 6", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по произведению двух простых чисел ===", out)
            self.assertIn("Результат - числа, являющиеся произведением двух простых чисел: [4, 6]", out)

    def test_run_happy_path_not_semiprime(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5 6", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по произведению двух простых чисел ===", out)
            self.assertIn("Результат - числа, НЕ являющиеся произведением двух простых чисел: [1, 2, 3, 5]", out)

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x 2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Ошибка: список чисел пуст", buf.getvalue())

    def test_run_no_semiprime_matches(self):
        with patch("builtins.input", side_effect=["1 2 3 5 7", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел, являющихся произведением двух простых чисел", buf.getvalue())

    def test_run_all_semiprime_matches(self):
        with patch("builtins.input", side_effect=["4 6 9", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Все числа являются произведением двух простых чисел", buf.getvalue())

    # -------- Класс SemiprimeFilter --------

    def test_class_init(self):
        sf = mod.SemiprimeFilter()
        self.assertEqual(sf.filter_type, "is_semiprime")
        sf = mod.SemiprimeFilter("not_semiprime")
        self.assertEqual(sf.filter_type, "not_semiprime")

    def test_class_set_filter_type_validation(self):
        sf = mod.SemiprimeFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'is_semiprime' или 'not_semiprime'"):
            sf.set_filter_type("BAD")
        sf.set_filter_type("is_semiprime")  # валидно

    def test_class_filter_delegates(self):
        sf = mod.SemiprimeFilter("is_semiprime")
        self.assertEqual(sf.filter([1, 2, 3, 4, 5, 6]), [4, 6])
        sf.set_filter_type("not_semiprime")
        self.assertEqual(sf.filter([1, 2, 3, 4, 5, 6]), [1, 2, 3, 5])

    def test_class_apply_calls_run(self):
        with patch("filters.math.semiprime_filter.run") as run_mock:
            mod.SemiprimeFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
