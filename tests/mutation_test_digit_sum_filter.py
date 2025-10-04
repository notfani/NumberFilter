"""
Мутационные тесты для фильтра суммы цифр
Проверяют качество существующих тестов путем внесения мутаций в код
"""

import unittest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from filters.digit_properties import digit_sum_filter


class MutationTestDigitSumFilter(unittest.TestCase):
    """
    Тесты с мутациями для проверки качества основных тестов
    """

    def setUp(self):
        self.test_numbers = [123, 456, 789, 12, 999, 100, 55]
        self.target_sum = 15

    def test_mutation_wrong_digit_sum_calculation(self):
        """Мутация: сумма заменена на произведение цифр"""
        def mutated_get_digit_sum(n):
            s = 1  # МУТАЦИЯ: начинаем с 1 вместо 0
            for digit in str(abs(n)):
                s *= int(digit)  # МУТАЦИЯ: умножение вместо сложения
            return s

        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            filtered_numbers = []
            for num in numbers:
                digit_sum = mutated_get_digit_sum(num)
                if filter_type == "equals":
                    if digit_sum == target_sum:
                        filtered_numbers.append(num)
                elif filter_type == "greater_than":
                    if digit_sum > target_sum:
                        filtered_numbers.append(num)
                elif filter_type == "less_than":
                    if digit_sum < target_sum:
                        filtered_numbers.append(num)
            return filtered_numbers

        original_result = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "equals")
        mutated_result = mutated_apply_filter(self.test_numbers, self.target_sum, "equals")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию сложения -> умножения")

    def test_mutation_wrong_comparison_operators(self):
        """Мутация: операторы сравнения перепутаны"""
        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            filtered_numbers = []
            for num in numbers:
                digit_sum = digit_sum_filter.get_digit_sum(num)
                if filter_type == "equals":
                    if digit_sum != target_sum:  # МУТАЦИЯ: == -> !=
                        filtered_numbers.append(num)
                elif filter_type == "greater_than":
                    if digit_sum < target_sum:  # МУТАЦИЯ: > -> <
                        filtered_numbers.append(num)
                elif filter_type == "less_than":
                    if digit_sum > target_sum:  # МУТАЦИЯ: < -> >
                        filtered_numbers.append(num)
            return filtered_numbers

        original_equals = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "equals")
        mutated_equals = mutated_apply_filter(self.test_numbers, self.target_sum, "equals")

        original_greater = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "greater_than")
        mutated_greater = mutated_apply_filter(self.test_numbers, self.target_sum, "greater_than")

        self.assertNotEqual(original_equals, mutated_equals,
                          "Тест должен обнаружить мутацию == -> !=")
        self.assertNotEqual(original_greater, mutated_greater,
                          "Тест должен обнаружить мутацию > -> <")

    def test_mutation_missing_abs(self):
        """Мутация: убрана функция abs() для отрицательных чисел"""
        def mutated_get_digit_sum(n):
            s = 0
            # МУТАЦИЯ: убрано abs() - обрабатываем отрицательные числа как есть
            str_n = str(n)
            if str_n.startswith('-'):
                # Считаем знак минус как отдельную "цифру" со значением 1
                s += 1
                str_n = str_n[1:]  # убираем знак минус

            for digit in str_n:
                s += int(digit)
            return s

        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            filtered_numbers = []
            for num in numbers:
                digit_sum = mutated_get_digit_sum(num)
                if filter_type == "equals":
                    if digit_sum == target_sum:
                        filtered_numbers.append(num)
            return filtered_numbers

        # Тест с отрицательными числами
        test_numbers_with_negative = [-123, 123, -456]

        # Оригинальная функция: -123 → abs(-123) → "123" → 1+2+3 = 6
        # Мутированная функция: -123 → "-123" → 1(за минус)+1+2+3 = 7

        # Ищем числа с суммой цифр = 6
        original_result = digit_sum_filter.apply_filter(test_numbers_with_negative, 6, "equals")
        mutated_result = mutated_apply_filter(test_numbers_with_negative, 6, "equals")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление abs()")

    def test_mutation_wrong_filter_type_logic(self):
        """Мутация: условия фильтрации перепутаны"""
        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            filtered_numbers = []
            for num in numbers:
                digit_sum = digit_sum_filter.get_digit_sum(num)
                if filter_type == "equals":
                    # МУТАЦИЯ: логика greater_than вместо equals
                    if digit_sum > target_sum:
                        filtered_numbers.append(num)
                elif filter_type == "greater_than":
                    # МУТАЦИЯ: логика less_than вместо greater_than
                    if digit_sum < target_sum:
                        filtered_numbers.append(num)
                elif filter_type == "less_than":
                    # МУТАЦИЯ: логика equals вместо less_than
                    if digit_sum == target_sum:
                        filtered_numbers.append(num)
            return filtered_numbers

        original_result = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "equals")
        mutated_result = mutated_apply_filter(self.test_numbers, self.target_sum, "equals")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить перестановку логики фильтрации")

    def test_mutation_boundary_conditions(self):
        """Мутация: >= заменено на >"""
        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            filtered_numbers = []
            for num in numbers:
                digit_sum = digit_sum_filter.get_digit_sum(num)
                if filter_type == "equals":
                    if digit_sum == target_sum:
                        filtered_numbers.append(num)
                elif filter_type == "greater_than":
                    if digit_sum >= target_sum:  # МУТАЦИЯ: > -> >=
                        filtered_numbers.append(num)
                elif filter_type == "less_than":
                    if digit_sum <= target_sum:  # МУТАЦИЯ: < -> <=
                        filtered_numbers.append(num)
            return filtered_numbers

        original_greater = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "greater_than")
        mutated_greater = mutated_apply_filter(self.test_numbers, self.target_sum, "greater_than")

        self.assertNotEqual(original_greater, mutated_greater,
                          "Тест должен обнаружить мутацию > -> >=")

    def test_mutation_empty_return(self):
        """Мутация: всегда возвращается пустой список"""
        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            return []  # МУТАЦИЯ: всегда пустой список

        original_result = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "equals")
        mutated_result = mutated_apply_filter(self.test_numbers, self.target_sum, "equals")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию возврата пустого списка")

    def test_mutation_return_all_numbers(self):
        """Мутация: возвращаются все числа независимо от условия"""
        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            return numbers  # МУТАЦИЯ: возвращаем все числа

        original_result = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "equals")
        mutated_result = mutated_apply_filter(self.test_numbers, self.target_sum, "equals")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию возврата всех чисел")

    def test_mutation_off_by_one_digit_sum(self):
        """Мутация: к сумме цифр добавляется 1"""
        def mutated_get_digit_sum(n):
            s = 0
            for digit in str(abs(n)):
                s += int(digit)
            return s + 1  # МУТАЦИЯ: добавляем 1

        def mutated_apply_filter(numbers, target_sum, filter_type="equals"):
            filtered_numbers = []
            for num in numbers:
                digit_sum = mutated_get_digit_sum(num)
                if filter_type == "equals":
                    if digit_sum == target_sum:
                        filtered_numbers.append(num)
            return filtered_numbers

        original_result = digit_sum_filter.apply_filter(self.test_numbers, self.target_sum, "equals")
        mutated_result = mutated_apply_filter(self.test_numbers, self.target_sum, "equals")

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию off-by-one в сумме цифр")


if __name__ == "__main__":
    unittest.main()
