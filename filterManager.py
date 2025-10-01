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
    elif sub_choice == 0:
        return
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")

def MathFilter(sub_choice: int):
    if sub_choice == 1:
        DivisibilityFilter()
    elif sub_choice == 2:
        SquareFilter()
    elif sub_choice == 3:
        PrimeFilter()
    elif sub_choice == 4:
        PowerFilter()
    elif sub_choice == 5:
        DivisorCountFilter()
    elif sub_choice == 6:
        SquareRootFilter()
    elif sub_choice == 7:
        FibonacciFilter()
    elif sub_choice == 8:
        SemiprimeFilter()
    elif sub_choice == 0:
        return
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")


def DigitPropertyFilter(sub_choice: int):
    if sub_choice == 1:
        DigitCountFilter()
    elif sub_choice == 2:
        DigitSumFilter()
    elif sub_choice == 3:
        PalindromeFilter()
    elif sub_choice == 4:
        DigitPlaceFilter()
    elif sub_choice == 5:
        DigitDifferenceFilter()
    elif sub_choice == 6:
        DigitAverageFilter()
    elif sub_choice == 7:
        DigitDeltaFilter()
    elif sub_choice == 0:
        return
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")


def SpecialFilter(sub_choice: int):
    if sub_choice == 1:
        SequenceFilter()
    elif sub_choice == 0:
        return
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")