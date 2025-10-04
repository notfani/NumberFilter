"""
Мутационные тесты для фильтра простых чисел
Проверяют качество существующих тестов путем внесения мутаций в код
"""

import unittest
import sys
import os
import math

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from filters.math import filter_primes


class MutationTestPrimesFilter(unittest.TestCase):
    """
    Тесты с мутациями для проверки качества основных тестов
    """

    def setUp(self):
        self.test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

    def test_mutation_wrong_base_case(self):
        """Мутация: граница n < 2 заменена на n < 1"""
        def mutated_is_prime(n: int) -> bool:
            if n < 1:  # МУТАЦИЯ: 2 -> 1
                return False
            if n % 2 == 0:
                return n == 2
            if n % 3 == 0:
                return n == 3
            r, f = math.isqrt(n), 5
            while f <= r:
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 6
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию базового случая n < 2 -> n < 1")

    def test_mutation_wrong_even_check(self):
        """Мутация: проверка четности убрана"""
        def mutated_is_prime(n: int) -> bool:
            if n < 2:
                return False
            # МУТАЦИЯ: убрана проверка четности
            if n % 3 == 0:
                return n == 3
            r, f = math.isqrt(n), 5
            while f <= r:
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 6
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление проверки четности")

    def test_mutation_wrong_divisor_increment(self):
        """Мутация: инкремент f += 6 заменен на f += 5"""
        def mutated_is_prime(n: int) -> bool:
            if n < 2:
                return False
            if n % 2 == 0:
                return n == 2
            if n % 3 == 0:
                return n == 3
            r, f = math.isqrt(n), 5
            while f <= r:
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 5  # МУТАЦИЯ: 6 -> 5
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию инкремента f += 6 -> f += 5")

    def test_mutation_wrong_starting_divisor(self):
        """Мутация: начальный делитель f = 5 заменен на f = 7"""
        def mutated_is_prime(n: int) -> bool:
            if n < 2:
                return False
            if n % 2 == 0:
                return n == 2
            if n % 3 == 0:
                return n == 3
            r, f = math.isqrt(n), 7  # МУТАЦИЯ: 5 -> 7
            while f <= r:
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 6
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию начального делителя f = 5 -> f = 7")

    def test_mutation_wrong_loop_condition(self):
        """Мутация: условие f <= r заменено на f < r"""
        def mutated_is_prime(n: int) -> bool:
            if n < 2:
                return False
            if n % 2 == 0:
                return n == 2
            if n % 3 == 0:
                return n == 3
            r, f = math.isqrt(n), 5
            while f < r:  # МУТАЦИЯ: <= -> <
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 6
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию условия цикла <= -> <")

    def test_mutation_missing_special_case_2(self):
        """Мутация: убрана специальная проверка для числа 2"""
        def mutated_is_prime(n: int) -> bool:
            if n < 2:
                return False
            if n % 2 == 0:
                return False  # МУТАЦИЯ: убрано n == 2
            if n % 3 == 0:
                return n == 3
            r, f = math.isqrt(n), 5
            while f <= r:
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 6
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление специального случая для 2")

    def test_mutation_missing_special_case_3(self):
        """Мутация: убрана специальная проверка для числа 3"""
        def mutated_is_prime(n: int) -> bool:
            if n < 2:
                return False
            if n % 2 == 0:
                return n == 2
            if n % 3 == 0:
                return False  # МУТАЦИЯ: убрано n == 3
            r, f = math.isqrt(n), 5
            while f <= r:
                if n % f == 0 or n % (f + 2) == 0:
                    return False
                f += 6
            return True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить удаление специального случая для 3")

    def test_mutation_return_all_numbers(self):
        """Мутация: функция всегда возвращает True"""
        def mutated_is_prime(n: int) -> bool:
            return True  # МУТАЦИЯ: всегда возвращаем True

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию всегда возвращающую True")

    def test_mutation_return_no_numbers(self):
        """Мутация: функция всегда возвращает False"""
        def mutated_is_prime(n: int) -> bool:
            return False  # МУТАЦИЯ: всегда возвращаем False

        def mutated_prime_filter(nums):
            return [x for x in nums if mutated_is_prime(x)]

        original_result = filter_primes.prime_filter(self.test_numbers)
        mutated_result = mutated_prime_filter(self.test_numbers)

        self.assertNotEqual(original_result, mutated_result,
                          "Тест должен обнаружить мутацию всегда возвращающую False")


if __name__ == "__main__":
    unittest.main()
