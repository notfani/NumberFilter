"""
Отбор чисел на основе разности между максимальной и минимальной цифрами
"""

def apply_filter(numbers, min_limit):
    if min_limit <= 0:
        print("Ошибка: порог должен быть как минимум 1")
        return []

    filtered_numbers = []

    for number in numbers:
        s_number = str(abs(number))
        digits = [int(ch) for ch in s_number if ch.isdigit()]
        if not digits:
            continue

        if (max(digits) - min(digits)) >= min_limit:
            filtered_numbers.append(number)

    return filtered_numbers


def get_user_input():
    try:
        min_limit = int(input("Введите минимальный порог разности (целое число ≥ 1): "))
    except ValueError:
        print("Ошибка: введите целое число")
        return None

    if min_limit <= 0:
        print("Ошибка: порог должен быть как минимум 1")
        return None

    return min_limit


def run():
    print("=== Фильтр по разности максимальной и минимальной цифры ===")
    print("Введите числа для фильтрации (через пробел):")

    try:
        numbers = list(map(int, input().split()))
    except ValueError:
        print("Ошибка: введите только целые числа")
        return

    if not numbers:
        print("Ошибка: список чисел пуст")
        return

    params = get_user_input()
    if params is None:
        return

    filtered_numbers = apply_filter(numbers, params)

    if filtered_numbers:
        print(f"Числа с разностью (max - min) меньше {params}: {filtered_numbers}")
    else:
        print(f"Нет чисел, у которых разность (max - min) меньше {params}")


class DigitDifferenceFilter:
    def __init__(self, min_limit):
        self.min_limit = min_limit

    def filter(self, numbers):
        if self.min_limit is None:
            raise ValueError("Минимальный порог разности не установлен")
        return apply_filter(numbers, self.min_limit)

    def apply(self):
        run()


if __name__ == "__main__":
    run()
