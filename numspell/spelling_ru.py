# -*- coding: utf-8 -*-
"""Russian rules and tables for the numspell module"""

from spelling import isnum, isorder


RULES = """
ab = {a0} {b}
axx = {a00} {x}
(a)xxx = {a} {*} {x}
"""

NUMBERS = {
    0: 'ноль',
    1: 'один',
    2: 'два',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    10: 'десять',
    11: 'одиннадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемьдесят',
    90: 'девяносто',
    100: 'сто',
    200: 'двести',
    300: 'триста',
    400: 'четыреста',
    500: 'пятьсот',
    600: 'шестьсот',
    700: 'семьсот',
    800: 'восемьсот',
    900: 'девятьсот',
}

ORDERS = [
    '',
    'тысяча', 'миллион', 'миллиард', 'триллион',
]

PASSES = """
^ 1 <order> = {}
1 <thousand> = одна тысяча
2 <thousand> = две тысячи
(1) <order> = {}
(<2-4>) <order> = {:pl_1}
<order> = {:pl_2}
"""

def _isthousand(x):
    return x == 1

def _between_2_and_4(x):
    return isnum(x) and 2 <= int(x) <= 4

def _make_plural_1(order):
    return (order == 'тысяча') and 'тысячи' or order + 'а'

def _make_plural_2(order):
    return (order == 'тысяча') and 'тысяч' or order + 'ов'

META = {
    "thousand~find" : _isthousand,
    "order~find": isorder,
    "order~replace": lambda x: ORDERS[x],
    "2-4~find": _between_2_and_4,
    "pl_1": _make_plural_1,
    "pl_2": _make_plural_2,
}

LIST_PASS = { 'passes': PASSES, 'meta': META }
