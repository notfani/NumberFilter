"""
Отбор чисел на основе разности между первой и последней цифрами
"""

def apply_filter(numbers, threshold):
    if threshold < 0 or threshold > 9:
        print("Ошибка: порог должен быть целым числом в диапазоне 0–9")
        return []

    filtered_numbers = []

    for number in numbers:
        s = str(abs(number))  # игнорируем знак
        first = int(s[0])
        last = int(s[-1])
        if abs(first + last) > threshold:
            filtered_numbers.append(number)

    return filtered_numbers


def get_user_input():
    try:
        threshold = int(input("Введите порог разности между первой и последней цифрами (целое 0–9): "))
    except ValueError:
        print("Ошибка: введите целое число")
        return None

    if threshold < 0 or threshold > 9:
        print("Ошибка: порог должен быть целым числом в диапазоне 0–9")
        return None

    return threshold


def run():
    print("=== Фильтр по разности первой и последней цифры ===")
    print("Введите числа для фильтрации (через пробел):")

    try:
        numbers = list(map(int, input().split()))
    except ValueError:
        print("Ошибка: введите только целые числа")
        return

    if not numbers:
        print("Ошибка: список чисел пуст")
        return

    threshold = get_user_input()
    if threshold is None:
        return

    filtered_numbers = apply_filter(numbers, threshold)

    if filtered_numbers:
        print(f"Числа, где |первая - последняя| > {threshold}: {filtered_numbers}")
    else:
        print(f"Нет чисел, где |первая - последняя| > {threshold}")


class DigitDeltaFilter:
    def __init__(self, threshold):
        self.threshold = threshold

    def filter(self, numbers):
        if self.threshold is None:
            raise ValueError("Порог разности не установлен")
        return apply_filter(numbers, self.threshold)

    def apply(self):
        run()


if __name__ == "__main__":
    run()
