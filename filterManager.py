from filters import *


def MainFilter(sub_choice: int):
    if sub_choice == 1:
        # Фильтр по диапазону
        filter = basic.range_filter.RangeFilter()
        filter.apply()
    elif sub_choice == 2:
        # Фильтр по четности
        filter = basic.parity_filter.ParityFilter()
        filter.apply()
    elif sub_choice == 3:
        # Фильтр по положительности/отрицательности
        positivity_filter = basic.positivity_filter.PositivityFilter()
        positivity_filter.apply()
    elif sub_choice == 4:
        # Фильтр по уникальности
        uniqueness_filter = basic.uniqueness_filter.UniquenessFilter()
        uniqueness_filter.apply()
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")

def MathFilter(sub_choice: int):
    if sub_choice == 1:
        # Фильтр по делимости
        math.divisibility_filter.run()
    elif sub_choice == 2:
        # Фильтр по квадратам
        filter = math.square_filter.SquareFilter()
        filter.apply()
    elif sub_choice == 3:
        # Фильтр простых чисел
        filter = math.filter_primes.PrimeFilter()
        filter.apply()
    elif sub_choice == 4:
        # Фильтр по степеням
        math.power_filter.run()
    elif sub_choice == 5:
        # Фильтр по количеству делителей
        math.divisor_count_filter.run()
    elif sub_choice == 6:
        # Фильтр по квадратным корням
        math.square_root_filter.run()
    elif sub_choice == 7:
        # Фильтр Фибоначчи
        math.fibonacci_filter.run()
    elif sub_choice == 8:
        # Фильтр полупростых чисел
        math.semiprime_filter.run()
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")


def DigitPropertyFilter(sub_choice: int):
    if sub_choice == 1:
        # Фильтр по количеству цифр
        digit_properties.digit_count_filter.run()
    elif sub_choice == 2:
        # Фильтр по сумме цифр
        digit_properties.digit_sum_filter.run()
    elif sub_choice == 3:
        # Фильтр палиндромов
        digit_properties.palindrome_filter.run()
    elif sub_choice == 4:
        # Фильтр по позиции цифры
        filter = digit_properties.digit_place_filter.DigitPlaceFilter()
        filter.apply()
    elif sub_choice == 5:
        # Фильтр по разности цифр
        digit_properties.digit_difference_filter.run()
    elif sub_choice == 6:
        # Фильтр по среднему значению цифр
        digit_properties.digit_average_filter.run()
    elif sub_choice == 7:
        # Фильтр по дельте цифр
        digit_properties.digit_delta_filter.run()
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")


def SpecialFilter(sub_choice: int):
    if sub_choice == 1:
        # Фильтр последовательностей
        special.sequence_filter.run()
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")