"""
Раннер для всех мутационных тестов
Запускает все мутационные тесты и показывает результаты
"""

import unittest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Импортируем все мутационные тесты
from tests.mutation_test_parity_filter import MutationTestParityFilter
from tests.mutation_test_range_filter import MutationTestRangeFilter
from tests.mutation_test_primes_filter import MutationTestPrimesFilter
from tests.mutation_test_digit_sum_filter import MutationTestDigitSumFilter
from tests.mutation_test_digit_average_filter import MutationTestDigitAverageFilter


def run_mutation_tests():
    """
    Запускает все мутационные тесты и выводит подробный отчет
    """
    print("=" * 60)
    print("ЗАПУСК МУТАЦИОННЫХ ТЕСТОВ")
    print("=" * 60)
    print()

    # Создаем тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тестовые классы
    test_classes = [
        MutationTestParityFilter,
        MutationTestRangeFilter,
        MutationTestPrimesFilter,
        MutationTestDigitSumFilter,
        MutationTestDigitAverageFilter
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    print()
    print("=" * 60)
    print("РЕЗУЛЬТАТЫ МУТАЦИОННОГО ТЕСТИРОВАНИЯ")
    print("=" * 60)

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = total_tests - failures - errors

    print(f"Всего тестов: {total_tests}")
    print(f"Успешных: {successes}")
    print(f"Неудачных: {failures}")
    print(f"Ошибок: {errors}")
    print()

    if failures > 0:
        print("ВНИМАНИЕ: Некоторые мутации НЕ ОБНАРУЖЕНЫ!")
        print("Это означает, что основные тесты могут быть неполными.")
        print()
        for test, traceback in result.failures:
            print(f"Неудачный тест: {test}")
            print("Описание проблемы:")
            print(traceback)
            print("-" * 40)

    if errors > 0:
        print("ОШИБКИ:")
        for test, traceback in result.errors:
            print(f"Ошибка в тесте: {test}")
            print(traceback)
            print("-" * 40)

    if failures == 0 and errors == 0:
        print("✅ ВСЕ МУТАЦИИ ОБНАРУЖЕНЫ!")
        print("Это означает, что основные тесты имеют хорошее покрытие.")

    print()
    print("=" * 60)
    print("ЧТО ОЗНАЧАЮТ РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    print("• Если мутационный тест ПРОШЕЛ - основные тесты ОБНАРУЖИЛИ мутацию (хорошо)")
    print("• Если мутационный тест ПРОВАЛИЛСЯ - основные тесты НЕ ОБНАРУЖИЛИ мутацию (плохо)")
    print("• Высокий процент обнаруженных мутаций = качественные тесты")
    print("• Низкий процент обнаруженных мутаций = тесты нуждаются в улучшении")

    return result


if __name__ == "__main__":
    run_mutation_tests()
