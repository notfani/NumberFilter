"""
Фильтр по четности - фильтрует числа на четные или нечетные.
"""

def apply_filter(numbers, filter_type):
    filtered_numbers = []

    if filter_type == "even":
        for num in numbers:
            # Ошибка: неправильная проверка четности - используем деление на 3 вместо 2
            if num % 3 == 0:
                filtered_numbers.append(num)
    elif filter_type == "odd":
        for num in numbers:
            if num % 2 != 0:
                filtered_numbers.append(num)
    else:
        print("Ошибка: неверный тип фильтрации. Используйте 'even' или 'odd'")
        return []

    return filtered_numbers

def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Четные числа")
    print("2. Нечетные числа")

    try:
        choice = int(input())
        if choice == 1:
            return "even"
        elif choice == 2:
            return "odd"
        else:
            print("Ошибка: выберите 1 или 2")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def run():
    print("=== Фильтр по четности ===")
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

    if filtered_numbers:
        type_name = "четные" if filter_type == "even" else "нечетные"
        print(f"{type_name.capitalize()} числа: {filtered_numbers}")
    else:
        type_name = "четных" if filter_type == "even" else "нечетных"
        print(f"Нет {type_name} чисел в списке")

class ParityFilter:

    def __init__(self, filter_type=None):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        if filter_type not in ["even", "odd"]:
            raise ValueError("filter_type должен быть 'even' или 'odd'")
        self.filter_type = filter_type

    def filter(self, numbers):
        if self.filter_type is None:
            raise ValueError("Тип фильтрации не установлен. Используйте set_filter_type()")

        return apply_filter(numbers, self.filter_type)

    def get_even_numbers(self, numbers):
        return apply_filter(numbers, "even")

    def get_odd_numbers(self, numbers):
        return apply_filter(numbers, "odd")

    def apply(self):
        run()

if __name__ == "__main__":
    run()
