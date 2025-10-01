"""
Фильтр по уникальности - фильтрует уникальные или повторяющиеся числа.
"""

def apply_filter(numbers, filter_type):
    filtered_numbers = []

    if filter_type == "unique":
        # Уникальные числа (встречаются только один раз)
        for num in numbers:
            if numbers.count(num) == 1:
                filtered_numbers.append(num)
    elif filter_type == "duplicates":
        # Повторяющиеся числа (убираем дубликаты, оставляем только один экземпляр)
        seen = set()
        for num in numbers:
            if num not in seen:
                seen.add(num)
                filtered_numbers.append(num)
    elif filter_type == "all_duplicates":
        # Все числа, которые встречаются более одного раза
        for num in numbers:
            if numbers.count(num) > 1 and num not in filtered_numbers:
                filtered_numbers.append(num)
    elif filter_type == "repeated_only":
        # Только повторяющиеся числа (все экземпляры)
        for num in numbers:
            if numbers.count(num) > 1:
                filtered_numbers.append(num)
    else:
        print("Ошибка: неверный тип фильтрации")
        return []

    return filtered_numbers

def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Уникальные числа (встречаются только один раз)")
    print("2. Убрать дубликаты (оставить только уникальные значения)")
    print("3. Числа, которые повторяются (без дубликатов)")
    print("4. Все повторяющиеся числа (включая все экземпляры)")

    try:
        choice = int(input())
        if choice == 1:
            return "unique"
        elif choice == 2:
            return "duplicates"
        elif choice == 3:
            return "all_duplicates"
        elif choice == 4:
            return "repeated_only"
        else:
            print("Ошибка: выберите число от 1 до 4")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def get_statistics(numbers):
    from collections import Counter

    counter = Counter(numbers)
    unique_count = sum(1 for count in counter.values() if count == 1)
    duplicate_count = sum(1 for count in counter.values() if count > 1)
    total_unique_values = len(counter)

    return {
        "total_numbers": len(numbers),
        "unique_values": total_unique_values,
        "unique_numbers": unique_count,
        "duplicate_numbers": duplicate_count,
        "most_common": counter.most_common(3)
    }

def run():
    """
    Основная функция для запуска фильтра по уникальности.
    """
    print("=== Фильтр по уникальности ===")
    print("Введите числа для фильтрации (через пробел):")

    try:
        numbers = list(map(int, input().split()))
    except ValueError:
        print("Ошибка: введите только целые числа")
        return

    if not numbers:
        print("Ошибка: список чисел пуст")
        return

    # Показываем статистику
    stats = get_statistics(numbers)
    print(f"\nСтатистика:")
    print(f"Всего чисел: {stats['total_numbers']}")
    print(f"Уникальных значений: {stats['unique_values']}")
    print(f"Чисел, встречающихся один раз: {stats['unique_numbers']}")
    print(f"Чисел, встречающихся несколько раз: {stats['duplicate_numbers']}")
    if stats['most_common']:
        print(f"Самые частые числа: {stats['most_common']}")
    print()

    filter_type = get_user_input()
    if filter_type is None:
        return

    filtered_numbers = apply_filter(numbers, filter_type)

    type_names = {
        "unique": "уникальные числа",
        "duplicates": "числа без дубликатов",
        "all_duplicates": "повторяющиеся числа",
        "repeated_only": "все повторяющиеся числа"
    }

    if filtered_numbers:
        type_name = type_names[filter_type]
        print(f"Результат ({type_name}): {filtered_numbers}")
    else:
        type_name = type_names[filter_type]
        print(f"Нет {type_name} в списке")

class UniquenessFilter:

    def __init__(self, filter_type=None):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        valid_types = ["unique", "duplicates", "all_duplicates", "repeated_only"]
        if filter_type not in valid_types:
            raise ValueError(f"filter_type должен быть одним из: {valid_types}")
        self.filter_type = filter_type

    def filter(self, numbers):
        if self.filter_type is None:
            raise ValueError("Тип фильтрации не установлен. Используйте set_filter_type()")

        return apply_filter(numbers, self.filter_type)

    def get_unique_numbers(self, numbers):
        return apply_filter(numbers, "unique")

    def remove_duplicates(self, numbers):
        return apply_filter(numbers, "duplicates")

    def get_duplicate_values(self, numbers):
        return apply_filter(numbers, "all_duplicates")

    def get_all_repeated(self, numbers):
        return apply_filter(numbers, "repeated_only")

    def get_statistics(self, numbers):
        return get_statistics(numbers)

    def apply(self):
        run()

if __name__ == "__main__":
    run()
