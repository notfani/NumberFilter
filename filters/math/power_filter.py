import math


def is_square(x: int) -> bool:
    if x < 0:
        return False
    r = math.isqrt(x)
    return r * r == x


def power_filter(numbers):
    return [x for x in numbers if is_square(x)]


def run():
    header = "~" * 10
    print(f"{header} Фильтр по степеням {header}")

    try:
        numbers = list(
            map(int, input("Введите числа для фильтрации через пробел: ").split())
        )
        if not numbers:
            raise ValueError("список чисел пуст")

        powers = power_filter(numbers)
        print(f"Найдено {len(powers)} степеней: {powers}")

    except ValueError as e:
        print(
            f"Ошибка: {'введите только целые числа' if 'invalid literal' in str(e) else str(e)}"
        )


def smoke_test():
    assert power_filter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [1, 4, 9]


smoke_test()
