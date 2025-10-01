"""
Фильтр по диапазону - фильтрует числа в заданном диапазоне.
"""

def apply_filter(numbers, min_value, max_value):
    if min_value > max_value:
        print("Ошибка: минимальное значение не может быть больше максимального")
        return []

    filtered_numbers = []
    for num in numbers:
        if min_value <= num <= max_value:
            filtered_numbers.append(num)

    return filtered_numbers

def get_user_input():
    print("Введите минимальное значение диапазона:")
    try:
        min_value = int(input())
    except ValueError:
        print("Ошибка: введите целое число")
        return None

    print("Введите максимальное значение диапазона:")
    try:
        max_value = int(input())
    except ValueError:
        print("Ошибка: введите целое число")
        return None

    return min_value, max_value

def run():
    print("=== Фильтр по диапазону ===")
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

    min_value, max_value = params

    filtered_numbers = apply_filter(numbers, min_value, max_value)

    if filtered_numbers:
        print(f"Числа в диапазоне от {min_value} до {max_value}: {filtered_numbers}")
    else:
        print(f"Нет чисел в диапазоне от {min_value} до {max_value}")

class RangeFilter:

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def set_range(self, min_value, max_value):
        """Устанавливает диапазон для фильтрации."""
        if min_value > max_value:
            raise ValueError("Минимальное значение не может быть больше максимального")
        self.min_value = min_value
        self.max_value = max_value

    def filter(self, numbers):
        if self.min_value is None or self.max_value is None:
            raise ValueError("Диапазон не установлен. Используйте set_range()")

        return apply_filter(numbers, self.min_value, self.max_value)

    def apply(self):
        run()

if __name__ == "__main__":
    run()
