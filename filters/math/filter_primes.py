import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n % 3 == 0:
        return n == 3
    r, f = math.isqrt(n), 5
    while f <= r:
        if n % f == 0 or n % (f + 2) == 0:
            return False
        f += 6
    return True


def prime_filter(nums):
    return [x for x in nums if is_prime(x)]


def run():
    header = "~" * 10
    print(f"{header} Фильтр простых чисел {header}")

    try:
        numbers = list(
            map(int, input("Введите числа для фильтрации через пробел: ").split())
        )
        if not numbers:
            raise ValueError("список чисел пуст")

        primes = prime_filter(numbers)
        print(f"Найдено {len(primes)} простых чисел: {primes}")

    except ValueError as e:
        print(
            f"Ошибка: {'введите только целые числа' if 'invalid literal' in str(e) else str(e)}"
        )


class PrimeFilter:
    def filter(self, numbers):
        return prime_filter(numbers)

    def apply(self):
        run()


def smoke_test():
    assert prime_filter([-5, -1, 0, 1, 11, 13, 15, 21, 23, 29]) == [11, 13, 23, 29]
