import unittest
import importlib

class MutationTestDigitAverageFilter(unittest.TestCase):
    def setUp(self):
        self.module = importlib.import_module('filters.digit_properties.digit_average_filter')
        self.filter_func = self.module.apply_filter
        self.numbers = [123, 456, 789, 111, 222, 333, 0, -123]

    def test_mutation_return_empty_list(self):
        # Мутация: функция всегда возвращает пустой список
        def mutated(numbers, min_avg):
            return []
        self.assertNotEqual(self.filter_func(self.numbers, 2), mutated(self.numbers, 2),
                            'Тест должен обнаружить возврат пустого списка')

    def test_mutation_wrong_comparison(self):
        # Мутация: сравнение avg > min_avg заменено на avg < min_avg
        def mutated(numbers, min_avg):
            result = []
            for n in numbers:
                s = str(abs(n))
                digits = [int(ch) for ch in s if ch.isdigit()]
                if not digits:
                    continue
                avg = sum(digits) / len(digits)
                if avg < min_avg:  # МУТАЦИЯ
                    result.append(n)
            return result
        original = self.filter_func(self.numbers, 2)
        mutated_result = mutated(self.numbers, 2)
        self.assertNotEqual(original, mutated_result, 'Тест должен обнаружить перепутанное сравнение')

    def test_mutation_return_all_numbers(self):
        # Мутация: функция всегда возвращает исходный список
        def mutated(numbers, min_avg):
            return list(numbers)
        self.assertNotEqual(self.filter_func(self.numbers, 2), mutated(self.numbers, 2),
                            'Тест должен обнаружить возврат исходного списка')
