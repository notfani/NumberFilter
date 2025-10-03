import math


def get_squares_until(n):
    return {i**2 for i in range(1, int(math.sqrt(n)))}


def square_filter(numbers):
    squares = get_squares_until(max(numbers))
    return [x for x in numbers if x in squares]


def run():
    header = "~" * 10
    print(f"{header} Фильтр по квадратам {header}")

    try:
        numbers = list(
            map(int, input("Введите числа для фильтрации через пробел: ").split())
        )
        if not numbers:
            raise ValueError("список чисел пуст")

        squares = square_filter(numbers)
        print(f"Найдено {len(squares)} квадратов: {squares}")

    except ValueError as e:
        print(
            f"Ошибка: {'введите только целые числа' if 'invalid literal' in str(e) else str(e)}"
        )


class SquareFilter:
    def filter(self, numbers):
        return square_filter(numbers)

    def apply(self):
        run()


def smoke_test():
    assert square_filter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [1, 4, 9]
