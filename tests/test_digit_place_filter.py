import unittest

import filters.digit_properties.digit_place_filter as mod


class TestDigitPlaceFilter(unittest.TestCase):
    # -------- digit_place_filter --------

    def test_digit_place_filter_from_left_basic(self):
        # Позиция 1 слева (первая цифра), ищем цифру 1
        # 123 - первая цифра 1, подходит
        # 456 - первая цифра 4, не подходит
        self.assertEqual(mod.digit_place_filter([123, 456, 178], 1, 1, True), [123, 178])

    def test_digit_place_filter_from_right_basic(self):
        # Позиция 1 справа (последняя цифра), ищем цифру 3
        # 123 - последняя цифра 3, подходит
        # 456 - последняя цифра 6, не подходит
        self.assertEqual(mod.digit_place_filter([123, 456, 783], 1, 3, False), [123, 783])

    def test_digit_place_filter_middle_position(self):
        # Позиция 2 слева (вторая цифра), ищем цифру 2
        # 123 - вторая цифра 2, подходит
        # 456 - вторая цифра 5, не подходит
        self.assertEqual(mod.digit_place_filter([123, 456, 928], 2, 2, True), [123, 928])

    def test_digit_place_filter_position_out_of_range(self):
        # Позиция 5, но число только трехзначное
        self.assertEqual(mod.digit_place_filter([123], 5, 1, True), [])

    def test_digit_place_filter_single_digit_number(self):
        # Однозначное число, позиция 1
        self.assertEqual(mod.digit_place_filter([5], 1, 5, True), [5])
        self.assertEqual(mod.digit_place_filter([5], 1, 3, True), [])

    def test_digit_place_filter_negative_numbers(self):
        # Отрицательные числа: берется abs()
        # -123 -> 123, первая цифра 1
        self.assertEqual(mod.digit_place_filter([-123], 1, 1, True), [-123])

    def test_digit_place_filter_invalid_position_zero(self):
        # Позиция 0 или отрицательная должна возвращать пустой список
        self.assertEqual(mod.digit_place_filter([123], 0, 1, True), [])

    def test_digit_place_filter_invalid_position_negative(self):
        self.assertEqual(mod.digit_place_filter([123], -1, 1, True), [])

    def test_digit_place_filter_invalid_digit_negative(self):
        # Цифра вне диапазона 0-9
        self.assertEqual(mod.digit_place_filter([123], 1, -1, True), [])

    def test_digit_place_filter_invalid_digit_too_large(self):
        self.assertEqual(mod.digit_place_filter([123], 1, 10, True), [])

    def test_digit_place_filter_empty_list(self):
        self.assertEqual(mod.digit_place_filter([], 1, 1, True), [])

    def test_digit_place_filter_from_right_position_2(self):
        # Позиция 2 справа (предпоследняя цифра), ищем цифру 2
        # 123 - предпоследняя цифра 2, подходит
        # 456 - предпоследняя цифра 5, не подходит
        self.assertEqual(mod.digit_place_filter([123, 456, 829], 2, 2, False), [123, 829])


class TestDigitPlaceFilterClass(unittest.TestCase):
    # -------- DigitPlaceFilter class --------

    def test_class_filter_basic(self):
        filter_obj = mod.DigitPlaceFilter(position=1, digit=1, from_left=True)
        self.assertEqual(filter_obj.filter([123, 456]), [123])

    def test_class_filter_no_position(self):
        filter_obj = mod.DigitPlaceFilter(digit=1, from_left=True)
        with self.assertRaises(ValueError):
            filter_obj.filter([123])

    def test_class_filter_no_digit(self):
        filter_obj = mod.DigitPlaceFilter(position=1, from_left=True)
        with self.assertRaises(ValueError):
            filter_obj.filter([123])


if __name__ == "__main__":
    unittest.main()
