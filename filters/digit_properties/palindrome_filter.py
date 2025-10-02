
"""
Фильтр по палиндромам - поиск палиндромных чисел (читающихся одинаково в обе стороны).
"""


def is_palindrome(n):
    s = str(abs(n))
    return s == s[::-1]

def apply_filter(numbers, filter_type="is_palindrome"):
    filtered_numbers = []
    for num in numbers:
        if filter_type == "is_palindrome":
            if is_palindrome(num):
                filtered_numbers.append(num)
        elif filter_type == "not_palindrome":
            if not is_palindrome(num):
                filtered_numbers.append(num)
    return filtered_numbers

def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Числа, являющиеся палиндромами")
    print("2. Числа, НЕ являющиеся палиндромами")

    try:
        choice = int(input())
        if choice == 1:
            return "is_palindrome"
        elif choice == 2:
            return "not_palindrome"
        else:
            print("Ошибка: выберите 1 или 2")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def run():
    print("=== Фильтр по палиндромам ===")
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

    if filter_type == "is_palindrome":
        if filtered_numbers:
            print(f"\nРезультат - числа-палиндромы: {filtered_numbers}")
        else:
            print("\nНет чисел-палиндромов")
    elif filter_type == "not_palindrome":
        if filtered_numbers:
            print(f"\nРезультат - числа, НЕ являющиеся палиндромами: {filtered_numbers}")
        else:
            print("\nВсе числа являются палиндромами")

class PalindromeFilter:
    def __init__(self, filter_type="is_palindrome"):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        if filter_type not in ["is_palindrome", "not_palindrome"]:
            raise ValueError("filter_type должен быть 'is_palindrome' или 'not_palindrome'")
        self.filter_type = filter_type

    def filter(self, numbers):
        return apply_filter(numbers, self.filter_type)

    def apply(self):
        run()

if __name__ == "__main__":
    run()

