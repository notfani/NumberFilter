# Пакет фильтров для обработки чисел
# Содержит четыре основных категорий
# basic - базовые фильтры
# math - математические фильтры
# digit_properties - фильтры по свойствам чисел
# special - специальные фильтры

from . import basic
from . import math
from . import digit_properties
from . import special

__all__ = ['basic', 'math', 'digit_properties', 'special']