import io
import unittest
from unittest.mock import patch

# Импортируем подмодуль явно, чтобы не зависеть от __all__
import filters.basic.positivity_filter as mod


class TestPositivityFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_apply_filter_positive(self):
        self.assertEqual(
            mod.apply_filter([-3, -1, 0, 1, 2, 5], "positive"),
            [1, 2, 5]
        )

    def test_apply_filter_negative(self):
        self.assertEqual(
            mod.apply_filter([-3, -1, 0, 1, 2, 5], "negative"),
            [-3, -1]
        )

    def test_apply_filter_zero(self):
        self.assertEqual(
            mod.apply_filter([-3, 0, 0, 4], "zero"),
            [0, 0]
        )

    def test_apply_filter_non_positive(self):
        # <= 0
        self.assertEqual(
            mod.apply_filter([-2, -1, 0, 1, 2], "non_positive"),
            [-2, -1, 0]
        )

    def test_apply_filter_non_negative(self):
        # >= 0
        self.assertEqual(
            mod.apply_filter([-2, -1, 0, 1, 2], "non_negative"),
            [0, 1, 2]
        )

    def test_apply_filter_invalid_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, -1, 0], "POS")
        self.assertEqual(res, [])
        self.assertIn("неверный тип фильтрации", buf.getvalue())

    # -------- get_user_input --------

    def test_get_user_input_choices(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "positive")
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "negative")
        with patch("builtins.input", return_value="3"):
            self.assertEqual(mod.get_user_input(), "zero")
        with patch("builtins.input", return_value="4"):
            self.assertEqual(mod.get_user_input(), "non_positive")
        with patch("builtins.input", return_value="5"):
            self.assertEqual(mod.get_user_input(), "non_negative")

    def test_get_user_input_wrong_number(self):
        with patch("builtins.input", return_value="6"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("выберите число от 1 до 5", buf.getvalue())

    def test_get_user_input_non_integer(self):
        with patch("builtins.input", return_value="x"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("введите целое число", buf.getvalue())

    # -------- run (интерактив) --------

    def test_run_happy_positive(self):
        with patch("builtins.input", side_effect=["-2 -1 0 1 2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Фильтр по положительности/отрицательности", out)
            self.assertIn("Положительные числа: [1, 2]", out)

    def test_run_no_matches_zero(self):
        with patch("builtins.input", side_effect=["1 2 3", "3"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Нет нули чисел в списке", buf.getvalue())  # "Нули" -> type_names['zero']

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x -2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("список чисел пуст", buf.getvalue())

    # -------- Класс PositivityFilter --------

    def test_class_filter_requires_type(self):
        pf = mod.PositivityFilter()
        with self.assertRaisesRegex(ValueError, "Тип фильтрации не установлен"):
            pf.filter([1, -1, 0])

    def test_class_set_filter_type_validation(self):
        pf = mod.PositivityFilter()
        with self.assertRaisesRegex(ValueError, "filter_type должен быть одним из"):
            pf.set_filter_type("POS")
        pf.set_filter_type("non_negative")  # валидно

    def test_class_filter_delegates(self):
        pf = mod.PositivityFilter("non_positive")
        self.assertEqual(pf.filter([-2, -1, 0, 1]), [-2, -1, 0])

    def test_class_helpers(self):
        pf = mod.PositivityFilter()
        self.assertEqual(pf.get_positive_numbers([-1, 0, 1, 2]), [1, 2])
        self.assertEqual(pf.get_negative_numbers([-2, -1, 0, 1]), [-2, -1])
        self.assertEqual(pf.get_zeros([-1, 0, 0, 1]), [0, 0])
        self.assertEqual(pf.get_non_positive_numbers([-2, -1, 0, 1]), [-2, -1, 0])
        self.assertEqual(pf.get_non_negative_numbers([-2, -1, 0, 1]), [0, 1])

    def test_class_apply_calls_run(self):
        with patch("filters.basic.positivity_filter.run") as run_mock:
            mod.PositivityFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
