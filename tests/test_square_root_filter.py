import io
import unittest
from unittest.mock import patch

import filters.math.square_root_filter as mod


class TestSquareRootFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_has_integer_sqrt(self):
        numbers = [0, 1, 2, 3, 4, 5, 9, 10, 16, -1, -4]
        expected = [0, 1, 4, 9, 16]
        self.assertEqual(mod.apply_filter(numbers), expected)

    def test_apply_filter_empty_list(self):
        self.assertEqual(mod.apply_filter([]), [])

    def test_apply_filter_no_integer_sqrt(self):
        numbers = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]
        expected = []
        self.assertEqual(mod.apply_filter(numbers), expected)

    # -------- get_user_input --------

    def test_get_user_input_has_integer_sqrt(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "has_integer_sqrt")

    def test_get_user_input_no_integer_sqrt(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "no_integer_sqrt")

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

    def test_run_happy_path_has_integer_sqrt(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по квадратным корням ===", out)
            self.assertIn("Результат - числа, имеющие целый квадратный корень: [1, 4]", out)

    def test_run_happy_path_no_integer_sqrt(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("=== Фильтр по квадратным корням ===", out)
            self.assertIn("Результат - числа, НЕ имеющие целый квадратный корень: [2, 3, 5]", out)

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

    def test_run_no_matches_has_integer_sqrt(self):
        with patch("builtins.input", side_effect=["2 3 5", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет чисел, имеющих целый квадратный корень", buf.getvalue())

    def test_run_all_matches_no_integer_sqrt(self):
        with patch("builtins.input", side_effect=["1 4 9", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Все числа имеют целый квадратный корень", buf.getvalue())

    # -------- Класс SquareRootFilter --------

    def test_class_init(self):
        srf = mod.SquareRootFilter()
        self.assertEqual(srf.filter_type, "has_integer_sqrt")
        srf = mod.SquareRootFilter("no_integer_sqrt")
        self.assertEqual(srf.filter_type, "no_integer_sqrt")

    def test_class_set_filter_type_validation(self):
        srf = mod.SquareRootFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'has_integer_sqrt' или 'no_integer_sqrt'"):
            srf.set_filter_type("BAD")
        srf.set_filter_type("has_integer_sqrt")  # валидно

    def test_class_filter_delegates(self):
        srf = mod.SquareRootFilter("has_integer_sqrt")
        self.assertEqual(srf.filter([1, 2, 3, 4, 5]), [1, 4])
        srf.set_filter_type("no_integer_sqrt")
        self.assertEqual(srf.filter([1, 2, 3, 4, 5]), [2, 3, 5])

    def test_class_apply_calls_run(self):
        with patch("filters.math.square_root_filter.run") as run_mock:
            mod.SquareRootFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
