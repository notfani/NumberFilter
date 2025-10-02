"""
Фильтрация чисел со средним значением цифр, превышающим заданное число
"""

def apply_filter(numbers, min_avg):
    if min_avg < 0:
        print("Ошибка: минимальное среднее значение не может быть отрицательным")
        return []

    filtered_numbers = []

    for number in numbers:
        s_number = str(abs(number))
        digits = [int(ch) for ch in s_number if ch.isdigit()]
        if not digits:
            continue

        avg = sum(digits) / len(digits)
        if avg > min_avg:
            filtered_numbers.append(number)

    return filtered_numbers

def get_user_input():
    raw = input("Введите минимальное среднее значение цифр (вещественное число ≥ 0): ")
    try:
        min_avg = float(raw.replace(",", "."))
    except ValueError:
        print("Ошибка: введите вещественное число")
        return None

    if min_avg < 0:
        print("Ошибка: минимальное среднее значение не может быть отрицательным")
        return None

    return min_avg

def run():
    print("=== Фильтр по среднему значению цифр ===")
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
        print(f"Числа со средним значением цифр больше {params}: {filtered_numbers}")
    else:
        print(f"Нет чисел со средним значением цифр больше {params}")


class DigitAverageFilter:
    def __init__(self, min_avg):
        self.min_avg = min_avg

    def filter(self, numbers):
        if self.min_avg is None:
            raise ValueError("Минимальное среднее значение не установлено")
        return apply_filter(numbers, self.min_avg)

    def apply(self):
        run()


if __name__ == "__main__":
    run()
