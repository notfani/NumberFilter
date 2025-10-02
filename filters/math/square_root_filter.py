
"""
Фильтр по квадратным корням - отбирает числа, имеющие целый квадратный корень.
"""
import math

def apply_filter(numbers):
    filtered_numbers = []
    for num in numbers:
        if num >= 0:
            sqrt_num = math.isqrt(num) # integer square root
            if sqrt_num * sqrt_num == num:
                filtered_numbers.append(num)
    return filtered_numbers

def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Числа, имеющие целый квадратный корень")
    print("2. Числа, НЕ имеющие целый квадратный корень")

    try:
        choice = int(input())
        if choice == 1:
            return "has_integer_sqrt"
        elif choice == 2:
            return "no_integer_sqrt"
        else:
            print("Ошибка: выберите 1 или 2")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def run():
    print("=== Фильтр по квадратным корням ===")
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

    if filter_type == "has_integer_sqrt":
        filtered_numbers = apply_filter(numbers)
        if filtered_numbers:
            print(f"\nРезультат - числа, имеющие целый квадратный корень: {filtered_numbers}")
        else:
            print("\nНет чисел, имеющих целый квадратный корень")
    elif filter_type == "no_integer_sqrt":
        all_numbers_with_sqrt = apply_filter(numbers)
        filtered_numbers = [num for num in numbers if num not in all_numbers_with_sqrt]
        if filtered_numbers:
            print(f"\nРезультат - числа, НЕ имеющие целый квадратный корень: {filtered_numbers}")
        else:
            print("\nВсе числа имеют целый квадратный корень")

class SquareRootFilter:
    def __init__(self, filter_type="has_integer_sqrt"):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        if filter_type not in ["has_integer_sqrt", "no_integer_sqrt"]:
            raise ValueError("filter_type должен быть 'has_integer_sqrt' или 'no_integer_sqrt'")
        self.filter_type = filter_type

    def filter(self, numbers):
        if self.filter_type == "has_integer_sqrt":
            return apply_filter(numbers)
        elif self.filter_type == "no_integer_sqrt":
            all_numbers_with_sqrt = apply_filter(numbers)
            return [num for num in numbers if num not in all_numbers_with_sqrt]

    def apply(self):
        run()

if __name__ == "__main__":
    run()
