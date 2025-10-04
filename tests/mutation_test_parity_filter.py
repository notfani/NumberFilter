"""
Мутационные тесты для фильтра четности
Проверяют качество существующих тестов путем внесения мутаций в код
"""

import unittest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from filters.basic import parity_filter


class MutationTestParityFilter(unittest.TestCase):
    """
    Тесты с мутациями для проверки качества основных тестов
    """

    def setUp(self):
        self.test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_mutation_wrong_modulo_operator(self):
        """Мутация: % заменен на //"""
        def mutated_apply_filter(numbers, filter_type):
            filtered_numbers = []
            if filter_type == "even":
                for num in numbers:
                    if num // 2 == 0:  # МУТАЦИЯ: % -> //
                        filtered_numbers.append(num)
            elif filter_type == "odd":
                for num in numbers:
                    if num // 2 != 0:  # МУТАЦИЯ: % -> //
                        filtered_numbers.append(num)
            else:
                return []
            return filtered_numbers

        # Проверяем, что мутированная версия дает другой результат
        original_result = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_result = mutated_apply_filter(self.test_numbers, "even")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию оператора % -> //")

    def test_mutation_wrong_comparison_operator(self):
        """Мутация: == заменен на !="""
        def mutated_apply_filter(numbers, filter_type):
            filtered_numbers = []
            if filter_type == "even":
                for num in numbers:
                    if num % 2 != 0:  # МУТАЦИЯ: == -> !=
                        filtered_numbers.append(num)
            elif filter_type == "odd":
                for num in numbers:
                    if num % 2 == 0:  # МУТАЦИЯ: != -> ==
                        filtered_numbers.append(num)
            else:
                return []
            return filtered_numbers

        original_even = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_even = mutated_apply_filter(self.test_numbers, "even")

        self.assertNotEqual(original_even, mutated_even,
                          "Тест должен обнаружить мутацию оператора == -> !=")

    def test_mutation_wrong_divisor(self):
        """Мутация: деление на 2 заменено на деление на 3"""
        def mutated_apply_filter(numbers, filter_type):
            filtered_numbers = []
            if filter_type == "even":
                for num in numbers:
                    if num % 3 == 0:  # МУТАЦИЯ: 2 -> 3
                        filtered_numbers.append(num)
            elif filter_type == "odd":
                for num in numbers:
                    if num % 3 != 0:  # МУТАЦИЯ: 2 -> 3
                        filtered_numbers.append(num)
            else:
                return []
            return filtered_numbers

        original_result = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_result = mutated_apply_filter(self.test_numbers, "even")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию константы 2 -> 3")

    def test_mutation_swapped_conditions(self):
        """Мутация: условия для четных и нечетных поменяны местами"""
        def mutated_apply_filter(numbers, filter_type):
            filtered_numbers = []
            if filter_type == "even":
                # МУТАЦИЯ: логика для нечетных чисел
                for num in numbers:
                    if num % 2 != 0:
                        filtered_numbers.append(num)
            elif filter_type == "odd":
                # МУТАЦИЯ: логика для четных чисел
                for num in numbers:
                    if num % 2 == 0:
                        filtered_numbers.append(num)
            else:
                return []
            return filtered_numbers

        original_even = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_even = mutated_apply_filter(self.test_numbers, "even")

        original_odd = parity_filter.apply_filter(self.test_numbers, "odd")
        mutated_odd = mutated_apply_filter(self.test_numbers, "odd")

        self.assertNotEqual(original_even, mutated_even,
                          "Тест должен обнаружить перестановку логики четных/нечетных")
        self.assertNotEqual(original_odd, mutated_odd,
                          "Тест должен обнаружить перестановку логики четных/нечетных")

    def test_mutation_return_empty_list(self):
        """Мутация: возвращается пустой список вместо фильтрованного"""
        def mutated_apply_filter(numbers, filter_type):
            return []  # МУТАЦИЯ: всегда возвращаем пустой список

        original_result = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_result = mutated_apply_filter(self.test_numbers, "even")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию возврата пустого списка")

    def test_mutation_return_original_list(self):
        """Мутация: возвращается исходный список без фильтрации"""
        def mutated_apply_filter(numbers, filter_type):
            return numbers  # МУТАЦИЯ: возвращаем исходный список

        original_result = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_result = mutated_apply_filter(self.test_numbers, "even")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию возврата исходного списка")

    def test_mutation_off_by_one(self):
        """Мутация: сравнение с 1 вместо 0"""
        def mutated_apply_filter(numbers, filter_type):
            filtered_numbers = []
            if filter_type == "even":
                for num in numbers:
                    if num % 2 == 1:  # МУТАЦИЯ: 0 -> 1
                        filtered_numbers.append(num)
            elif filter_type == "odd":
                for num in numbers:
                    if num % 2 != 1:  # МУТАЦИЯ: 0 -> 1
                        filtered_numbers.append(num)
            else:
                return []
            return filtered_numbers

        original_result = parity_filter.apply_filter(self.test_numbers, "even")
        mutated_result = mutated_apply_filter(self.test_numbers, "even")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию off-by-one (0 -> 1)")


if __name__ == "__main__":
    unittest.main()
