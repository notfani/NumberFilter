# Фильтры по свойствам цифр числа.


from .digit_count_filter import DigitCountFilter
from .digit_sum_filter import DigitSumFilter
from .palindrome_filter import PalindromeFilter
from .digit_place_filter import DigitPlaceFilter
from .digit_difference_filter import DigitDifferenceFilter
from .digit_average_filter import DigitAverageFilter
from .digit_delta_filter import DigitDeltaFilter

__all__ = [
    'DigitCountFilter',
    'DigitSumFilter',
    'PalindromeFilter',
    'DigitPlaceFilter',
    'DigitDifferenceFilter',
    'DigitAverageFilter',
    'DigitDeltaFilter'
]
