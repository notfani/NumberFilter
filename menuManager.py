import sys
import filterManager

def kill():
    print("I'm dead now...")
    sys.exit(0)

def PrintMenu():
    print("Выберете действие:")
    print("1. Основные фильтры")
    print("2. Математические фильтры")
    print("3. Фильтр по свойствам цифр")
    print("4. Специальные фильтры")
    print("0. Выход")

def PrintSubMenu(filter_type):
    if filter_type == 1:
        print("Основные фильтры:")
        print("1. Фильтр по диапазону")
        print("2. Фильтр по четности")
        print("3. Фильтр по положительности/отрицательности")
        print("4. Фильтр по уникальности")
        print("0. Вернуться в главное меню")
    elif filter_type == 2:
        print("Математические фильтры:")
        print("1. Фильтр по делимости")
        print("2. Фильтр по квадратам")
        print("3. Фильтр по простоте")
        print("4. Фильтр по степени")
        print("5. Фильтр по количеству делителей")
        print("6. Фильтр по квадратным корням")
        print("7. Фильтр по числам Фибоначчи")
        print("8. Фильтр по произведению двух простых чисел")
        print("0. Вернуться в главное меню")
    elif filter_type == 3:
        print("Фильтры по свойствам цифр:")
        print("1. Фильтр по количеству цифр")
        print("2. Фильтр по сумме цифр")
        print("3. Фильтр по палиндромам")
        print("4. Фильтр по разрядам")
        print("5. Фильтр по разнице между цифрами")
        print("6. Фильтр по среднему значению цифр")
        print("7. Фильтр по разности цифр")
        print("0. Вернуться в главное меню")
    elif filter_type == 4:
        print("Специальные фильтры:")
        print("1. Фильтр по последовательности")
        print("0. Вернуться в главное меню")

def CatchInput():
    while True:
        try:
            user_input = int(input())
            if not user_input:
                print("Ошибка: Пустой ввод. Попробуйте ещё раз.")
                continue
            else:
                return user_input
        except ValueError:
            print("Ошибка: Введите только целые числа. Попробуйте ещё раз.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}. Попробуйте ещё раз.")

def InputManager(choice: int):
    if choice == 1:
        PrintSubMenu(1)
        sub_choice = CatchInput()
        filterManager.MainFilter(sub_choice)
        return None
    elif choice == 2:
        PrintSubMenu(2)
        sub_choice = CatchInput()
        filterManager.MathFilter(sub_choice)
        return None
    elif choice == 3:
        PrintSubMenu(3)
        sub_choice = CatchInput()
        filterManager.DigitPropertyFilter(sub_choice)
        return None
    elif choice == 4:
        PrintSubMenu(4)
        sub_choice = CatchInput()
        filterManager.SpecialFilter(sub_choice)
        return None
    elif choice == 0:
        kill()
        return None
    else:
        print("Ошибка: Неверный выбор. Попробуйте ещё раз.")
        return None
