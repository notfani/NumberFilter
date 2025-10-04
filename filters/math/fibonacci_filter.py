"""
Фильтр по числам Фибоначчи - поиск чисел, являющихся частью последовательности Фибоначчи.
"""

from math import isqrt


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def is_fibonacci(n: int) -> bool:
    # n — число Фибоначчи, если 5*n^2 + 4 ИЛИ 5*n^2 - 4 — полный квадрат
    if n < 0:
        return False
    x = 5 * n * n
    return is_perfect_square(x + 4) or is_perfect_square(x - 4)


def apply_filter(numbers, filter_type="is_fibonacci"):
    filtered_numbers = []
    for num in numbers:
        if filter_type == "is_fibonacci":
            if is_fibonacci(num):
                filtered_numbers.append(num)
        elif filter_type == "not_fibonacci":
            if not is_fibonacci(num):
                filtered_numbers.append(num)
        else:
            print("Ошибка: неверный тип фильтрации. Используйте 'is_fibonacci' или 'not_fibonacci'")
            return []
    return filtered_numbers


def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Числа, являющиеся числами Фибоначчи")
    print("2. Числа, НЕ являющиеся числами Фибоначчи")

    try:
        choice = int(input())
        if choice == 1:
            return "is_fibonacci"
        elif choice == 2:
            return "not_fibonacci"
        else:
            print("Ошибка: выберите 1 или 2")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None


def run():
    print("=== Фильтр по числам Фибоначчи ===")
    print("Введите числа для фильтрации (через пробел):")

    try:
        numbers = list(map(int, input().split()))
    except ValueError:
        print("Ошибка: введите только целые числа")
        return

    if not numbers:
        print("Ошибка: список чисел пуст")
        return

    filter_type = get_user_input()
    if filter_type is None:
        return

    filtered_numbers = apply_filter(numbers, filter_type)

    if filter_type == "is_fibonacci":
        if filtered_numbers:
            print(f"\nРезультат - числа Фибоначчи: {filtered_numbers}")
        else:
            print("\nНет чисел Фибоначчи")
    elif filter_type == "not_fibonacci":
        if filtered_numbers:
            print(f"\nРезультат - числа, НЕ являющиеся числами Фибоначчи: {filtered_numbers}")
        else:
            print("\nВсе числа являются числами Фибоначчи")


class FibonacciFilter:
    def __init__(self, filter_type="is_fibonacci"):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        if filter_type not in ["is_fibonacci", "not_fibonacci"]:
            raise ValueError("filter_type должен быть 'is_fibonacci' или 'not_fibonacci'")
        self.filter_type = filter_type

    def filter(self, numbers):
        return apply_filter(numbers, self.filter_type)

    def apply(self):
        run()


if __name__ == "__main__":
    run()
