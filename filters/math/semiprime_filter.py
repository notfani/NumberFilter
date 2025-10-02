
"""
Фильтр по произведению двух простых чисел - отбор чисел, являющихся произведением двух простых чисел.
"""

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_semiprime(n):
    if n < 4:
        return False
    prime_factors = []
    temp_n = n
    d = 2
    while d * d <= temp_n:
        if temp_n % d == 0:
            prime_factors.append(d)
            temp_n //= d
        else:
            d += 1
    if temp_n > 1:
        prime_factors.append(temp_n)

    # A semiprime is a natural number that is the product of two prime numbers.
    # The two primes can be the same.
    return len(prime_factors) == 2 and is_prime(prime_factors[0]) and is_prime(prime_factors[1])

def apply_filter(numbers, filter_type="is_semiprime"):
    filtered_numbers = []
    for num in numbers:
        if filter_type == "is_semiprime":
            if is_semiprime(num):
                filtered_numbers.append(num)
        elif filter_type == "not_semiprime":
            if not is_semiprime(num):
                filtered_numbers.append(num)
    return filtered_numbers

def get_user_input():
    print("Выберите тип фильтрации:")
    print("1. Числа, являющиеся произведением двух простых чисел")
    print("2. Числа, НЕ являющиеся произведением двух простых чисел")

    try:
        choice = int(input())
        if choice == 1:
            return "is_semiprime"
        elif choice == 2:
            return "not_semiprime"
        else:
            print("Ошибка: выберите 1 или 2")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None

def run():
    print("=== Фильтр по произведению двух простых чисел ===")
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

    if filter_type == "is_semiprime":
        if filtered_numbers:
            print(f"\nРезультат - числа, являющиеся произведением двух простых чисел: {filtered_numbers}")
        else:
            print("\nНет чисел, являющихся произведением двух простых чисел")
    elif filter_type == "not_semiprime":
        if filtered_numbers:
            print(f"\nРезультат - числа, НЕ являющиеся произведением двух простых чисел: {filtered_numbers}")
        else:
            print("\nВсе числа являются произведением двух простых чисел")

class SemiprimeFilter:
    def __init__(self, filter_type="is_semiprime"):
        self.filter_type = filter_type

    def set_filter_type(self, filter_type):
        if filter_type not in ["is_semiprime", "not_semiprime"]:
            raise ValueError("filter_type должен быть 'is_semiprime' или 'not_semiprime'")
        self.filter_type = filter_type

    def filter(self, numbers):
        return apply_filter(numbers, self.filter_type)

    def apply(self):
        run()

if __name__ == "__main__":
    run()
