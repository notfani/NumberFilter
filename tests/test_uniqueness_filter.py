import io
import unittest
from unittest.mock import patch

# Явный импорт подмодуля — не зависит от __all__
import filters.basic.uniqueness_filter as mod


class TestUniquenessFilter(unittest.TestCase):
    # -------- apply_filter --------

    def test_unique_only_once(self):
        # 1 и 4 встречаются ровно один раз
        self.assertEqual(
            mod.apply_filter([1, 2, 2, 3, 3, 3, 4], "unique"),
            [1, 4]
        )

    def test_duplicates_remove_dupes_keep_order(self):
        # "duplicates" = удалить дубликаты, оставить первые вхождения (порядок исходный)
        self.assertEqual(
            mod.apply_filter([3, 3, 2, 1, 2, 1, 1], "duplicates"),
            [3, 2, 1]
        )

    def test_all_duplicates_distinct_values(self):
        # Значения, у которых частота > 1, по одному разу
        self.assertEqual(
            mod.apply_filter([1, 1, 2, 2, 2, 3, 4, 4], "all_duplicates"),
            [1, 2, 4]
        )

    def test_repeated_only_all_instances(self):
        # Все повторяющиеся экземпляры (исключая одиночные)
        self.assertEqual(
            mod.apply_filter([1, 1, 2, 3, 3, 3, 4], "repeated_only"),
            [1, 1, 3, 3, 3]
        )

    def test_apply_filter_with_negatives_and_zero(self):
        nums = [-2, -2, -1, 0, 0, 1, 2]
        self.assertEqual(mod.apply_filter(nums, "unique"), [-1, 1, 2])
        self.assertEqual(mod.apply_filter(nums, "duplicates"), [-2, -1, 0, 1, 2])
        self.assertEqual(mod.apply_filter(nums, "all_duplicates"), [-2, 0])
        self.assertEqual(mod.apply_filter(nums, "repeated_only"), [-2, -2, 0, 0])

    def test_apply_filter_invalid_type(self):
        with patch("sys.stdout", new_callable=io.StringIO) as buf:
            res = mod.apply_filter([1, 1, 2], "bad")
        self.assertEqual(res, [])
        self.assertIn("неверный тип фильтрации", buf.getvalue())

    # -------- get_user_input --------

    def test_get_user_input_choices(self):
        with patch("builtins.input", return_value="1"):
            self.assertEqual(mod.get_user_input(), "unique")
        with patch("builtins.input", return_value="2"):
            self.assertEqual(mod.get_user_input(), "duplicates")
        with patch("builtins.input", return_value="3"):
            self.assertEqual(mod.get_user_input(), "all_duplicates")
        with patch("builtins.input", return_value="4"):
            self.assertEqual(mod.get_user_input(), "repeated_only")

    def test_get_user_input_wrong_number(self):
        with patch("builtins.input", return_value="5"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("выберите число от 1 до 4", buf.getvalue())

    def test_get_user_input_non_integer(self):
        with patch("builtins.input", return_value="x"), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            self.assertIsNone(mod.get_user_input())
            self.assertIn("введите целое число", buf.getvalue())

    # -------- get_statistics --------

    def test_get_statistics(self):
        stats = mod.get_statistics([1, 1, 2, 3, 3, 3])
        self.assertEqual(stats["total_numbers"], 6)
        self.assertEqual(stats["unique_values"], 3)         # {1,2,3}
        self.assertEqual(stats["unique_numbers"], 1)        # только "2" одиночный
        self.assertEqual(stats["duplicate_numbers"], 2)     # значения 1 и 3 повторяются
        self.assertTrue(isinstance(stats["most_common"], list))
        self.assertEqual(stats["most_common"][0][0], 3)     # самое частое значение — 3

    # -------- run (интерактив) --------

    def test_run_happy_all_duplicates(self):
        # числа -> выбор "3" (all_duplicates)
        with patch("builtins.input", side_effect=["1 1 2 3 3 3", "3"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            out = buf.getvalue()
            self.assertIn("Фильтр по уникальности", out)
            self.assertIn("Статистика", out)
            self.assertIn("Всего чисел: 6", out)
            self.assertIn("Уникальных значений: 3", out)
            self.assertIn("Результат (повторяющиеся числа): [1, 3]", out)

    def test_run_invalid_numbers_input(self):
        with patch("builtins.input", side_effect=["1 x 2", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("введите только целые числа", buf.getvalue())

    def test_run_empty_numbers(self):
        with patch("builtins.input", side_effect=["", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            self.assertIn("список чисел пуст", buf.getvalue())

    def test_run_no_matches_unique(self):
        with patch("builtins.input", side_effect=["1 1", "1"]), \
             patch("sys.stdout", new_callable=io.StringIO) as buf:
            mod.run()
            # Текстовой шаблон как в модуле (да, грамматика ломает уши, но это ожидаемое поведение)
            self.assertIn("Нет уникальные числа в списке", buf.getvalue())

    # -------- Класс UniquenessFilter --------

    def test_class_filter_requires_type(self):
        uf = mod.UniquenessFilter()
        with self.assertRaisesRegex(ValueError, "Тип фильтрации не установлен"):
            uf.filter([1, 2, 3])

    def test_class_set_filter_type_validation(self):
        uf = mod.UniquenessFilter()
        with self.assertRaisesRegex(ValueError, "должен быть одним из"):
            uf.set_filter_type("BAD")
        uf.set_filter_type("unique")  # валидно

    def test_class_filter_delegates(self):
        uf = mod.UniquenessFilter("repeated_only")
        self.assertEqual(uf.filter([1, 1, 2, 3, 3]), [1, 1, 3, 3])

    def test_class_helpers(self):
        uf = mod.UniquenessFilter()
        self.assertEqual(uf.get_unique_numbers([1, 1, 2, 3, 3, 4]), [2, 4])
        self.assertEqual(uf.remove_duplicates([1, 1, 2, 2, 2, 3]), [1, 2, 3])
        self.assertEqual(uf.get_duplicate_values([1, 1, 2, 3, 3]), [1, 3])
        self.assertEqual(uf.get_all_repeated([1, 1, 2, 3, 3]), [1, 1, 3, 3])

    def test_class_apply_calls_run(self):
        with patch("filters.basic.uniqueness_filter.run") as run_mock:
            mod.UniquenessFilter().apply()
            run_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
