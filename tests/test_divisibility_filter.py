import io
import unittest
from unittest.mock import patch

import filters.math.divisibility_filter as mod


class TestDivisibilityFilter(unittest.TestCase):
    # ---------- apply_filter ----------

    def test_apply_filter_divisible(self):
        self.assertEqual(mod.apply_filter([3, 4, 6, 9, 10, 12], 3, "divisible"), [3, 6, 9, 12])

    def test_apply_filter_not_divisible(self):
        self.assertEqual(mod.apply_filter([3, 4, 6, 9, 10, 12], 3, "not_divisible"), [4, 10])

    def test_apply_filter_divisor_zero(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 2, 3], 0, "divisible")
        self.assertEqual(res, [])
        self.assertIn("деление на ноль невозможно", buf.getvalue())

    def test_apply_filter_negative_divisor_behaves_like_positive(self):
        nums = [-6, -5, 0, 5, 6]
        self.assertEqual(mod.apply_filter(nums, 5, "divisible"), mod.apply_filter(nums, -5, "divisible"))
        self.assertEqual(mod.apply_filter(nums, 5, "not_divisible"), mod.apply_filter(nums, -5, "not_divisible"))

    def test_apply_filter_invalid_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 2, 3], 2, "BAD")
        self.assertEqual(res, [])
        self.assertIn("неверный тип фильтрации", buf.getvalue())

    # ---------- find_common_divisors ----------

    def test_find_common_divisors_basic(self):
        self.assertEqual(mod.find_common_divisors([12, 18, 24]), [1, 2, 3, 6])

    def test_find_common_divisors_with_zeroes(self):
        self.assertEqual(mod.find_common_divisors([0, 0, 12]), [1, 2, 3, 4, 6, 12])

    def test_find_common_divisors_negatives(self):
        self.assertEqual(mod.find_common_divisors([-4, 8, -12]), [1, 2, 4])

    def test_find_common_divisors_empty_or_all_zero(self):
        self.assertEqual(mod.find_common_divisors([]), [])
        self.assertEqual(mod.find_common_divisors([0, 0]), [])

    # ---------- get_user_input ----------

    def test_get_user_input_valid_paths(self):
        with patch("builtins.input", side_effect=["5", "1"]):
            self.assertEqual(mod.get_user_input(), (5, "divisible"))
        with patch("builtins.input", side_effect=["7", "2"]):
            self.assertEqual(mod.get_user_input(), (7, "not_divisible"))

    def test_get_user_input_divisor_zero(self):
        with patch("builtins.input", side_effect=["0"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("делитель не может быть равен нулю", buf.getvalue())

    def test_get_user_input_invalids(self):
        with patch("builtins.input", side_effect=["x"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("введите целое число", buf.getvalue())

        with patch("builtins.input", side_effect=["5", "3"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("выберите 1 или 2", buf.getvalue())

    # ---------- show_divisibility_analysis ----------

    def test_show_divisibility_analysis_prints_counts_and_remainders(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.show_divisibility_analysis([6, 10, 15], 5)
            out = buf.getvalue()
            self.assertIn("Анализ делимости на 5", out)
            self.assertIn("Делятся: 2 чисел - [10, 15]", out)
            self.assertIn("Не делятся: 1 чисел - [6]", out)
            self.assertIn("Остатки от деления:", out)
            self.assertIn("Остаток 1: [6]", out)

    # ---------- run (interactive) ----------

    def test_run_happy_divisible_and_common_divisors(self):
        # Числа имеют общие делители > 1, делитель выбираем 8, тип 1 (делятся)
        with patch("builtins.input", side_effect=["8 16 32", "8", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Общие делители всех чисел: [1, 2, 4, 8]", out)
            self.assertIn("Результат - числа, делящиеся на 8: [8, 16, 32]", out)

    def test_run_not_divisible_branch(self):
        with patch("builtins.input", side_effect=["1 2 3 4", "2", "2"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("Результат - числа, не делящиеся на 2: [1, 3]", buf.getvalue())

    def test_run_invalid_numbers(self):
        with patch("builtins.input", side_effect=["1 x 2", "2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("список чисел пуст", buf.getvalue())

    # ---------- Класс DivisibilityFilter ----------

    def test_class_requires_divisor(self):
        f = mod.DivisibilityFilter()
        with self.assertRaisesRegex(ValueError, "Делитель не установлен"):
            f.filter([1, 2, 3])

    def test_class_setters_validation(self):
        f = mod.DivisibilityFilter()
        with self.assertRaisesRegex(ValueError, "Делитель не может быть равен нулю"):
            f.set_divisor(0)
        with self.assertRaisesRegex(ValueError, "filter_type должен быть 'divisible' или 'not_divisible'"):
            f.set_filter_type("BAD")
        f.set_divisor(3)
        f.set_filter_type("not_divisible")  # валидно

    def test_class_filter_and_helpers(self):
        f = mod.DivisibilityFilter(3, "divisible")
        self.assertEqual(f.filter([3, 4, 5, 6]), [3, 6])
        self.assertEqual(f.get_divisible_numbers([3, 4, 5, 6], 2), [4, 6])
        self.assertEqual(f.get_not_divisible_numbers([3, 4, 5, 6], 2), [3, 5])

    def test_class_analyze_and_apply_call(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.DivisibilityFilter().analyze_divisibility([1, 2, 3], 2)
            self.assertIn("Анализ делимости на 2", buf.getvalue())
        with patch("filters.math.divisibility_filter.run") as run_mock:
            mod.DivisibilityFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
