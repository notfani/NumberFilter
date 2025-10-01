"""
Фильтр по положительности/отрицательности - фильтрует числа по знаку.
"""

def apply_filter(numbers, filter_type):

    filtered_numbers = []

    if filter_type == "positive":
        for num in numbers:
            if num > 0:
                filtered_numbers.append(num)
    elif filter_type == "negative":
        for num in numbers:
            if num < 0:
                filtered_numbers.append(num)
    elif filter_type == "zero":
        for num in numbers:
            if num == 0:
                filtered_numbers.append(num)
    elif filter_type == "non_positive":
        for num in numbers:
            if num <= 0:
                filtered_numbers.append(num)
    elif filter_type == "non_negative":
        for num in numbers:
            if num >= 0:
                filtered_numbers.append(num)
    else:
        print("Ошибка: неверный тип фильтрации")
        return []

    return filtered_numbers

def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Положительные числа (> 0)")
    print("2. Отрицательные числа (< 0)")
    print("3. Нули (= 0)")
    print("4. Неположительные числа (<= 0)")
    print("5. Неотрицательные числа (>= 0)")

    try:
        choice = int(input())
        if choice == 1:
            return "positive"
        elif choice == 2:
            return "negative"
        elif choice == 3:
            return "zero"
        elif choice == 4:
            return "non_positive"
        elif choice == 5:
            return "non_negative"
        else:
            print("Ошибка: выберите число от 1 до 5")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def run():
    """
    Основная функция для запуска фильтра по положительности.
    """
    print("=== Фильтр по положительности/отрицательности ===")
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

    type_names = {
        "positive": "положительные",
        "negative": "отрицательные",
        "zero": "нули",
        "non_positive": "неположительные",
        "non_negative": "неотрицательные"
    }

    if filtered_numbers:
        type_name = type_names[filter_type]
        print(f"{type_name.capitalize()} числа: {filtered_numbers}")
    else:
        type_name = type_names[filter_type]
        print(f"Нет {type_name} чисел в списке")

class PositivityFilter:

    def __init__(self, filter_type=None):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        valid_types = ["positive", "negative", "zero", "non_positive", "non_negative"]
        if filter_type not in valid_types:
            raise ValueError(f"filter_type должен быть одним из: {valid_types}")
        self.filter_type = filter_type

    def filter(self, numbers):
        if self.filter_type is None:
            raise ValueError("Тип фильтрации не установлен. Используйте set_filter_type()")

        return apply_filter(numbers, self.filter_type)

    def get_positive_numbers(self, numbers):
        return apply_filter(numbers, "positive")

    def get_negative_numbers(self, numbers):
        return apply_filter(numbers, "negative")

    def get_zeros(self, numbers):
        return apply_filter(numbers, "zero")

    def get_non_positive_numbers(self, numbers):
        return apply_filter(numbers, "non_positive")

    def get_non_negative_numbers(self, numbers):
        return apply_filter(numbers, "non_negative")

    def apply(self):
        run()

if __name__ == "__main__":
    run()
