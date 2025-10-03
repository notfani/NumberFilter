"""Фильтр по значению цифры в разряде."""


def digit_place_filter(numbers, position, digit, from_left=True):
    if position <= 0 or not (0 <= digit <= 9):
        return []

    index = position - 1 if from_left else -position
    result = []
    for number in numbers:
        s = str(abs(number))
        if len(s) > abs(index):
            if int(s[index]) == digit:
                result.append(number)
    return result


def run():
    print("=== Фильтр по значению цифры в разряде ===")
    try:
        numbers = list(map(int, input("Числа: ").split()))
        position = int(input("Позиция (>=1): "))
        digit = int(input("Цифра (0-9): "))
        from_left = input("Сторона (L/R): ").strip().upper() != "R"
    except ValueError:
        print("Ошибка: введите целые числа")
        return

    result = digit_place_filter(numbers, position, digit, from_left)
    print("Результат:", result if result else "пусто")


class DigitPlaceFilter:
    def __init__(self, position=None, digit=None, from_left=True):
        self.position = position
        self.digit = digit
        self.from_left = from_left

    def filter(self, numbers):
        if self.position is None or self.digit is None:
            raise ValueError("Не заданы позиция или цифра")
        return digit_place_filter(numbers, self.position, self.digit, self.from_left)

    def apply(self):
        run()


if __name__ == "__main__":
    run()
