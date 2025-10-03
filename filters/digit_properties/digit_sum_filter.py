
"""
Фильтр по сумме цифр - отбор чисел на основе суммы их цифр.
"""


def get_digit_sum(n):
    s = 0
    for digit in str(abs(n)):
        s += int(digit)
    return s

def apply_filter(numbers, target_sum, filter_type="equals"):
    filtered_numbers = []
    for num in numbers:
        digit_sum = get_digit_sum(num)
        if filter_type == "equals":
            if digit_sum == target_sum:
                filtered_numbers.append(num)
        elif filter_type == "greater_than":
            if digit_sum > target_sum:
                filtered_numbers.append(num)
        elif filter_type == "less_than":
            if digit_sum < target_sum:
                filtered_numbers.append(num)
    return filtered_numbers

def get_user_input():
    print("Введите целевую сумму цифр:")
    try:
        target_sum = int(input())
    except ValueError:
        print("Ошибка: введите целое число")
        return None, None

    print("Выберите тип фильтрации:")
    print("1. Сумма цифр равна", target_sum)
    print("2. Сумма цифр больше", target_sum)
    print("3. Сумма цифр меньше", target_sum)

    try:
        choice = int(input())
        if choice == 1:
            return target_sum, "equals"
        elif choice == 2:
            return target_sum, "greater_than"
        elif choice == 3:
            return target_sum, "less_than"
        else:
            print("Ошибка: выберите 1, 2 или 3")
            return None, None
    except ValueError:
        print("Ошибка: введите целое число")
        return None, None

def run():
    print("=== Фильтр по сумме цифр ===")
    print("Введите числа для фильтрации (через пробел):")

    try:
        numbers = list(map(int, input().split()))
    except ValueError:
        print("Ошибка: введите только целые числа")
        return

    if not numbers:
        print("Ошибка: список чисел пуст")
        return

    target_sum, filter_type = get_user_input()
    if target_sum is None or filter_type is None:
        return

    filtered_numbers = apply_filter(numbers, target_sum, filter_type)

    type_name = "равна" if filter_type == "equals" else ("больше" if filter_type == "greater_than" else "меньше")

    if filtered_numbers:
        print(f"\nРезультат - числа, сумма цифр которых {type_name} {target_sum}: {filtered_numbers}")
    else:
        print(f"\nНет чисел, сумма цифр которых {type_name} {target_sum}")

class DigitSumFilter:
    def __init__(self, target_sum=None, filter_type="equals"):
        self.target_sum = target_sum
        self.filter_type = filter_type

    def set_target_sum(self, target_sum):
        self.target_sum = target_sum

    def set_filter_type(self, filter_type):
        if filter_type not in ["equals", "greater_than", "less_than"]:
            raise ValueError("filter_type должен быть 'equals', 'greater_than' или 'less_than'")
        self.filter_type = filter_type

    def filter(self, numbers):
        if self.target_sum is None:
            raise ValueError("Целевая сумма цифр не установлена. Используйте set_target_sum()")
        return apply_filter(numbers, self.target_sum, self.filter_type)

    def apply(self):
        run()

if __name__ == "__main__":
    run()
