import io
import unittest
from unittest.mock import patch

# Импортируем подмодуль явно (не зависит от __all__)
import filters.basic.parity_filter as mod


class TestParityFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_even_basic(self):
        self.assertEqual(mod.apply_filter([1, 2, 3, 4, 5, 6], "even"), [2, 4, 6])

    def test_apply_filter_odd_basic(self):
        self.assertEqual(mod.apply_filter([1, 2, 3, 4, 5, 6], "odd"), [1, 3, 5])

    def test_apply_filter_zero_is_even(self):
        self.assertEqual(mod.apply_filter([0, 1, 2], "even"), [0, 2])

    def test_apply_filter_with_negatives(self):
        # Чётность для отрицательных корректна: -4 чётное, -3 нечётное
        self.assertEqual(mod.apply_filter([-5, -4, -3, -2, -1], "even"), [-4, -2])
        self.assertEqual(mod.apply_filter([-5, -4, -3, -2, -1], "odd"), [-5, -3, -1])

    def test_apply_filter_invalid_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 2, 3], "EVEN")  # неверное значение
        self.assertEqual(res, [])
        self.assertIn("неверный тип фильтрации", buf.getvalue())

    # -------- get_user_input --------

    def test_get_user_input_even_choice(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "even")

    def test_get_user_input_odd_choice(self):
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "odd")

    def test_get_user_input_wrong_number(self):
        with patch("builtins.input", return_value="3"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("выберите 1 или 2", buf.getvalue())

    def test_get_user_input_non_integer(self):
        with patch("builtins.input", return_value="x"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("введите целое число", buf.getvalue())

    # -------- run (интерактив) --------

    def test_run_even_happy_path(self):
        with patch("builtins.input", side_effect=["1 2 3 4 5", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Фильтр по четности", out)
            self.assertIn("Четные числа: [2, 4]", out)  # capitalize() -> "Четные"

    def test_run_odd_no_matches(self):
        with patch("builtins.input", side_effect=["2 4 6 8", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет нечетных чисел в списке", buf.getvalue())

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x 3", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("список чисел пуст", buf.getvalue())

    # -------- Класс ParityFilter --------

    def test_class_filter_requires_type(self):
        pf = mod.ParityFilter()
        with self.assertRaisesRegex(ValueError, "Тип фильтрации не установлен"):
            pf.filter([1, 2, 3])

    def test_class_set_filter_type_validation(self):
        pf = mod.ParityFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'even' или 'odd'"):
            pf.set_filter_type("EVEN")
        pf.set_filter_type("even")  # не должно упасть

    def test_class_filter_even(self):
        pf = mod.ParityFilter("even")
        self.assertEqual(pf.filter([1, 2, 3, 4]), [2, 4])

    def test_class_helpers(self):
        pf = mod.ParityFilter()
        self.assertEqual(pf.get_even_numbers([1, 2, 3, 4]), [2, 4])
        self.assertEqual(pf.get_odd_numbers([1, 2, 3, 4]), [1, 3])

    def test_class_apply_calls_run(self):
        with patch("filters.basic.parity_filter.run") as run_mock:
            mod.ParityFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
