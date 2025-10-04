"""
Мутационные тесты для фильтра диапазона
Проверяют качество существующих тестов путем внесения мутаций в код
"""

import unittest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from filters.basic import range_filter


class MutationTestRangeFilter(unittest.TestCase):
    """
    Тесты с мутациями для проверки качества основных тестов
    """

    def setUp(self):
        self.test_numbers = [1, 5, 10, 15, 20, 25, 30]
        self.min_val = 10
        self.max_val = 20

    def test_mutation_wrong_comparison_operators(self):
        """Мутация: <= заменен на <"""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value > max_value:
                return []
            filtered_numbers = []
            for num in numbers:
                if min_value < num < max_value:  # МУТАЦИЯ: <= num <= -> < num <
                    filtered_numbers.append(num)
            return filtered_numbers

        original_result = range_filter.apply_filter(self.test_numbers, self.min_val, self.max_val)
        mutated_result = mutated_apply_filter(self.test_numbers, self.min_val, self.max_val)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию <= -> <")

    def test_mutation_boundary_check_removed(self):
        """Мутация: проверка границ удалена"""
        def mutated_apply_filter(numbers, min_value, max_value):
            # МУТАЦИЯ: убрана проверка min_value > max_value
            filtered_numbers = []
            for num in numbers:
                if min_value <= num <= max_value:
                    filtered_numbers.append(num)
            return filtered_numbers

        # Тест с неправильными границами
        original_result = range_filter.apply_filter(self.test_numbers, 20, 10)
        mutated_result = mutated_apply_filter(self.test_numbers, 20, 10)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление проверки границ")

    def test_mutation_swapped_boundaries(self):
        """Мутация: границы поменяны местами"""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value > max_value:
                return []
            filtered_numbers = []
            for num in numbers:
                if max_value <= num <= min_value:  # МУТАЦИЯ: границы поменяны
                    filtered_numbers.append(num)
            return filtered_numbers

        original_result = range_filter.apply_filter(self.test_numbers, self.min_val, self.max_val)
        mutated_result = mutated_apply_filter(self.test_numbers, self.min_val, self.max_val)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить перестановку границ")

    def test_mutation_wrong_boundary_comparison(self):
        """Мутация: > заменен на >="""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value >= max_value:  # МУТАЦИЯ: > -> >=
                return []
            filtered_numbers = []
            for num in numbers:
                if min_value <= num <= max_value:
                    filtered_numbers.append(num)
            return filtered_numbers

        # Тест с равными границами
        original_result = range_filter.apply_filter(self.test_numbers, 15, 15)
        mutated_result = mutated_apply_filter(self.test_numbers, 15, 15)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию > -> >=")

    def test_mutation_only_min_boundary(self):
        """Мутация: проверяется только минимальная граница"""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value > max_value:
                return []
            filtered_numbers = []
            for num in numbers:
                if min_value <= num:  # МУТАЦИЯ: убрана проверка максимума
                    filtered_numbers.append(num)
            return filtered_numbers

        original_result = range_filter.apply_filter(self.test_numbers, self.min_val, self.max_val)
        mutated_result = mutated_apply_filter(self.test_numbers, self.min_val, self.max_val)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление проверки максимума")

    def test_mutation_only_max_boundary(self):
        """Мутация: проверяется только максимальная граница"""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value > max_value:
                return []
            filtered_numbers = []
            for num in numbers:
                if num <= max_value:  # МУТАЦИЯ: убрана проверка минимума
                    filtered_numbers.append(num)
            return filtered_numbers

        original_result = range_filter.apply_filter(self.test_numbers, self.min_val, self.max_val)
        mutated_result = mutated_apply_filter(self.test_numbers, self.min_val, self.max_val)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление проверки минимума")

    def test_mutation_negated_condition(self):
        """Мутация: условие отфильтровано наоборот"""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value > max_value:
                return []
            filtered_numbers = []
            for num in numbers:
                if not (min_value <= num <= max_value):  # МУТАЦИЯ: добавлен not
                    filtered_numbers.append(num)
            return filtered_numbers

        original_result = range_filter.apply_filter(self.test_numbers, self.min_val, self.max_val)
        mutated_result = mutated_apply_filter(self.test_numbers, self.min_val, self.max_val)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить инверсию условия")

    def test_mutation_return_all_numbers(self):
        """Мутация: возвращаются все числа независимо от условия"""
        def mutated_apply_filter(numbers, min_value, max_value):
            if min_value > max_value:
                return []
            return numbers  # МУТАЦИЯ: возвращаем все числа

        original_result = range_filter.apply_filter(self.test_numbers, self.min_val, self.max_val)
        mutated_result = mutated_apply_filter(self.test_numbers, self.min_val, self.max_val)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить возврат всех чисел")


if __name__ == "__main__":
    unittest.main()
