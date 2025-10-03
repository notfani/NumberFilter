"""Фильтр по количеству делителей."""

import math


def divisor_count(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0

    limit = int(math.isqrt(n))
    count = 0
    for i in range(1, limit + 1):
        if n % i == 0:
            count += 2 if i * i != n else 1
    return count


def divisor_count_filter(numbers, target, mode="equals"):
    if target <= 0 or mode not in {"equals", "greater", "less"}:
        return []

    cmp = {
        "equals": lambda c: c == target,
        "greater": lambda c: c > target,
        "less": lambda c: c < target,
    }[mode]
    return [n for n in numbers if cmp(divisor_count(n))]


def run():
    print("=== Фильтр по количеству делителей ===")
    try:
        numbers = list(map(int, input("Числа: ").split()))
        target = int(input("Целевое количество делителей: "))
        mode_choice = input("Режим (=, >, <): ").strip()
    except ValueError:
        print("Ошибка: введите целые числа")
        return

    mode_alias = {"=": "equals", "==": "equals", ">": "greater", "<": "less"}
    mode = mode_alias.get(mode_choice, mode_choice)
    result = divisor_count_filter(numbers, target, mode)
    print("Результат:", result if result else "пусто")


class DivisorCountFilter:
    def __init__(self, target=None, mode="equals"):
        self.target = target
        self.mode = mode

    def filter(self, numbers):
        if self.target is None:
            raise ValueError("Не задано целевое количество делителей")
        return divisor_count_filter(numbers, self.target, self.mode)

    def apply(self):
        run()


if __name__ == "__main__":
    run()
