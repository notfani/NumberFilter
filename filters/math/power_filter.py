import math


def is_perfect_power(value: int) -> bool:
    if value <= 1:
        return value == 1

    exponents = []
    n = value
    divisor = 2

    while divisor * divisor <= n:
        count = 0
        while n % divisor == 0:
            n //= divisor
            count += 1
        if count:
            exponents.append(count)
        divisor = 3 if divisor == 2 else divisor + 2

    if n > 1:
        exponents.append(1)

    if not exponents:
        return False

    gcd = exponents[0]
    for exp in exponents[1:]:
        gcd = math.gcd(gcd, exp)
    return gcd > 1


def power_filter(numbers):
    return [x for x in numbers if x > 0 and is_perfect_power(x)]


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


class PowerFilter:
    def filter(self, numbers):
        return power_filter(numbers)

    def apply(self):
        run()


def smoke_test():
    assert power_filter([1, 2, 3, 4, 5, 8, 9, 16, 27, 32]) == [1, 4, 8, 9, 16, 27, 32]
