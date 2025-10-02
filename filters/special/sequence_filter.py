"""
Поиск чисел, принадлежащих заданной последовательности (арифметической или геометрической).

Арифметическая прогрессия: a_n = a1 + (n-1)*d, n >= 1
Геометрическая прогрессия: a_n = a1 * r^(n-1), n >= 1
"""

def _is_in_arith(x: int, a1: int, d: int) -> bool:
    if d == 0:
        return x == a1
    diff = x - a1
    # x принадлежит АП, если (x - a1) кратно d и (n-1) >= 0
    return diff % d == 0 and (diff // d) >= 0


def _is_power_by_ratio(y: int, r: int) -> bool:
    """
    Проверяет, что существует k >= 0: y == r^k (для целых y,r, r != 0).
    Работает и для отрицательных r.
    """
    if y == 1:
        return True  # k = 0
    if r in (1, -1):
        # r = 1: только 1; r = -1: 1, -1 -> но y==1 уже отловили
        return y == -1 if r == -1 else False
    # Общее целочисленное деление
    while y != 1:
        if r == 0 or y % r != 0:
            return False
        y //= r
    return True


def _is_in_geom(x: int, a1: int, r: int) -> bool:
    # Особые случаи
    if a1 == 0:
        return x == 0  # 0, 0, 0, ...
    if r == 0:
        # a1, 0, 0, 0, ...
        return x == a1 or x == 0
    if r == 1:
        return x == a1
    if r == -1:
        return x == a1 or x == -a1

    # Общее правило: x/a1 должно быть целым и равным r^(k), k >= 0
    if x % a1 != 0:
        return False
    y = x // a1
    return _is_power_by_ratio(y, r)


def apply_filter(numbers, params):
    """
    params: кортеж (seq_type, a1, step)
      - seq_type: 'A' (арифметическая) или 'G' (геометрическая)
      - a1: первый член (int)
      - step: d для AП или r для ГП (int)
    """
    if not isinstance(params, tuple) or len(params) != 3:
        print("Ошибка: некорректные параметры фильтра")
        return []

    seq_type, a1, step = params
    if seq_type not in ("A", "G"):
        print("Ошибка: тип должен быть 'A' (арифм.) или 'G' (геом.)")
        return []

    filtered = []
    for x in numbers:
        if seq_type == "A":
            if _is_in_arith(x, a1, step):
                filtered.append(x)
        else:  # "G"
            if _is_in_geom(x, a1, step):
                filtered.append(x)
    return filtered


def get_user_input():
    t = input("Введите тип последовательности (A — арифм., G — геом.): ").strip().upper()
    # Поддержим также русские буквы
    if t == "А":
        t = "A"
    if t == "Г":
        t = "G"

    if t not in ("A", "G"):
        print("Ошибка: тип должен быть 'A' или 'G'")
        return None

    try:
        a1 = int(input("Введите первый член a1 (целое число): ").strip())
    except ValueError:
        print("Ошибка: a1 должен быть целым числом")
        return None

    if t == "A":
        try:
            d = int(input("Введите разность d (целое число, можно 0): ").strip())
        except ValueError:
            print("Ошибка: d должен быть целым числом")
            return None
        return (t, a1, d)
    else:
        try:
            r = int(input("Введите знаменатель r (целое число, можно 0, ±1): ").strip())
        except ValueError:
            print("Ошибка: r должен быть целым числом")
            return None
        return (t, a1, r)


def run():
    print("=== Фильтр по принадлежности арифм./геом. последовательности ===")
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

    result = apply_filter(numbers, params)

    seq_type, a1, step = params
    if seq_type == "A":
        desc = f"АП(a1={a1}, d={step})"
    else:
        desc = f"ГП(a1={a1}, r={step})"

    if result:
        print(f"Числа, принадлежащие {desc}: {result}")
    else:
        print(f"Нет чисел, принадлежащих {desc}")


class SequenceFilter:
    def __init__(self, seq_type, a1, step):
        """
        seq_type: 'A' или 'G'
        a1: первый член (int)
        step: d (для 'A') или r (для 'G')
        """
        if seq_type not in ("A", "G"):
            raise ValueError("seq_type должен быть 'A' или 'G'")
        self.seq_type = seq_type
        self.a1 = int(a1)
        self.step = int(step)

    def filter(self, numbers):
        return apply_filter(numbers, (self.seq_type, self.a1, self.step))

    def apply(self):
        run()


if __name__ == "__main__":
    run()
