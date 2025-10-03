"""
Фильтр по указанному количеству разрядов
"""

def apply_filter(numbers, digit_amount):
    if digit_amount <= 0:
        print("Ошибка: в числе должен быть как минимум 1 разряд")
        return []

    filtered_numbers = []
    for num in numbers:
        if len(str(abs(num))) == digit_amount:
            filtered_numbers.append(num)

    return filtered_numbers

def get_user_input():
    try:
        digit_amount = int(input("Введите количество разрядов:"))
    except ValueError:
        print("Ошибка: введите целое число")
        return None

    return digit_amount

def run():
    print("=== Фильтр по разрядам ===")
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
        print(f"Числа с {params} разрядами: {filtered_numbers}")
    else:
        print(f"Нет чисел с разрядом {params}")


class DigitCountFilter:
    def __init__(self, digit_amount):
        self.digit_amount = digit_amount

    def filter(self, numbers):
        if self.digit_amount is None:
            raise ValueError("Количество разрядов не установлено")

        return apply_filter(numbers, self.digit_amount)

    def apply(self):
        run()


if __name__ == "__main__":
    run()