"""
Фильтр по делимости - фильтрует числа, которые делятся на заданное число.
"""

def apply_filter(numbers, divisor, filter_type="divisible"):
    if divisor == 0:
        print("Ошибка: деление на ноль невозможно")
        return []

    filtered_numbers = []

    if filter_type == "divisible":
        for num in numbers:
            if num % divisor == 0:
                filtered_numbers.append(num)
    elif filter_type == "not_divisible":
        for num in numbers:
            if num % divisor != 0:
                filtered_numbers.append(num)
    else:
        print("Ошибка: неверный тип фильтрации. Используйте 'divisible' или 'not_divisible'")
        return []

    return filtered_numbers

def find_common_divisors(numbers):
    if not numbers:
        return []

    # Исключаем нули для корректного вычисления НОД
    non_zero_numbers = [num for num in numbers if num != 0]
    if not non_zero_numbers:
        return []

    from math import gcd
    from functools import reduce

    # Находим НОД всех чисел
    common_gcd = reduce(gcd, [abs(num) for num in non_zero_numbers])

    # Находим все делители НОД
    divisors = []
    for i in range(1, abs(common_gcd) + 1):
        if common_gcd % i == 0:
            divisors.append(i)

    return divisors

def get_user_input():
    print("Введите число-делитель:")
    try:
        divisor = int(input())
        if divisor == 0:
            print("Ошибка: делитель не может быть равен нулю")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

    print("Выберите тип фильтрации:")
    print("1. Числа, которые делятся на", divisor)
    print("2. Числа, которые НЕ делятся на", divisor)

    try:
        choice = int(input())
        if choice == 1:
            return divisor, "divisible"
        elif choice == 2:
            return divisor, "not_divisible"
        else:
            print("Ошибка: выберите 1 или 2")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def show_divisibility_analysis(numbers, divisor):
    divisible = apply_filter(numbers, divisor, "divisible")
    not_divisible = apply_filter(numbers, divisor, "not_divisible")

    print(f"\nАнализ делимости на {divisor}:")
    print(f"Делятся: {len(divisible)} чисел - {divisible}")
    print(f"Не делятся: {len(not_divisible)} чисел - {not_divisible}")

    if divisible:
        remainders = {}
        for num in not_divisible:
            remainder = num % divisor
            if remainder in remainders:
                remainders[remainder].append(num)
            else:
                remainders[remainder] = [num]

        if remainders:
            print(f"Остатки от деления:")
            for remainder, nums in sorted(remainders.items()):
                print(f"  Остаток {remainder}: {nums}")

def run():
    print("=== Фильтр по делимости ===")
    print("Введите числа для фильтрации (через пробел):")

    try:
        numbers = list(map(int, input().split()))
    except ValueError:
        print("Ошибка: введите только целые числа")
        return

    if not numbers:
        print("Ошибка: список чисел пуст")
        return

    # Показываем общие делители
    common_divs = find_common_divisors(numbers)
    if common_divs and len(common_divs) > 1:
        print(f"Общие делители всех чисел: {common_divs}")

    params = get_user_input()
    if params is None:
        return

    divisor, filter_type = params

    # Показываем анализ
    show_divisibility_analysis(numbers, divisor)

    filtered_numbers = apply_filter(numbers, divisor, filter_type)

    type_name = "делящиеся" if filter_type == "divisible" else "не делящиеся"

    if filtered_numbers:
        print(f"\nРезультат - числа, {type_name} на {divisor}: {filtered_numbers}")
    else:
        print(f"\nНет чисел, {type_name} на {divisor}")

class DivisibilityFilter:
    def __init__(self, divisor=None, filter_type="divisible"):
        self.divisor = divisor
        self.filter_type = filter_type

    def set_divisor(self, divisor):
        if divisor == 0:
            raise ValueError("Делитель не может быть равен нулю")
        self.divisor = divisor

    def set_filter_type(self, filter_type):
        if filter_type not in ["divisible", "not_divisible"]:
            raise ValueError("filter_type должен быть 'divisible' или 'not_divisible'")
        self.filter_type = filter_type

    def filter(self, numbers):
        if self.divisor is None:
            raise ValueError("Делитель не установлен. Используйте set_divisor()")

        return apply_filter(numbers, self.divisor, self.filter_type)

    def get_divisible_numbers(self, numbers, divisor):
        return apply_filter(numbers, divisor, "divisible")

    def get_not_divisible_numbers(self, numbers, divisor):
        return apply_filter(numbers, divisor, "not_divisible")

    def find_common_divisors(self, numbers):
        return find_common_divisors(numbers)

    def analyze_divisibility(self, numbers, divisor):
        show_divisibility_analysis(numbers, divisor)

    def apply(self):
        run()

if __name__ == "__main__":
    run()
