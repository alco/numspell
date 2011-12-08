# -*- coding: utf-8 -*-
"""Spanish rules and tables for the spellnum module"""

RULES = """
ab = {a0} y {b}
axx = {a00} {x}
  1xxx = {1000} {x}
axxx = {a} mil {x}
  21xxx = veintiún {1000} {x}
aaxxx = {a} {1000} {x}
  100xxx = cien {1000} {x}
  101xxx = ciento un {1000} {x}
aaaxxx = {a} mil {x}
(a)xxxxxx = {a} {x}
"""
##  'a--xxx = {a} mil {x}

NUMBERS = {
    0: 'cero',
    1: 'uno',
    2: 'dos',
    3: 'tres',
    4: 'cuatro',
    5: 'cinco',
    6: 'seis',
    7: 'siete',
    8: 'ocho',
    9: 'nueve',
    10: 'diez',
    11: 'once',
    12: 'doce',
    13: 'trece',
    14: 'catorce',
    15: 'quince',
    16: 'dieciséis',
    17: 'diecisiete',
    18: 'dieciocho',
    19: 'diecinueve',
    20: 'veinte',
    21: 'veintiuno',
    22: 'veintidós',
    23: 'veintitrés',
    24: 'veinticuatro',
    25: 'veinticinco',
    26: 'veintiséis',
    27: 'veintisiete',
    28: 'veintiocho',
    29: 'veintinueve',
    30: 'treinta',
    40: 'cuarenta',
    50: 'cincuenta',
    60: 'sesenta',
    70: 'setenta',
    80: 'ochenta',
    90: 'noventa',
    100: 'ciento',
    200: 'doscientos',
    300: 'trescientos',
    400: 'cuatrocientos',
    500: 'quinientos',
    600: 'seiscientos',
    700: 'setecientos',
    800: 'ochocientos',
    900: 'novecientos',
    1000: 'mil',
}

ORDERS = [
    '',
    'millón', 'billón', 'trillón', 'cuatrillón',
    'quintillón', 'sextillón', 'septillón', 'octillón', 'nonillón',
    'decillón', 'undecillón', 'duodecillón', 'tredecillón',
    'cuatordecillón', 'quindecillón'
]

PREORDERS = {
    1: 'un',
    21: 'veintiún',
    101: 'cientoún',
    100: 'cien',
}

def ORDERMAP(num, order):
    if num == 1:
        return order
    return order.replace('ón', 'ones')

def pl(order):
    return order.replace('ón', 'ones')

PASSES = """
^ 1 mil = mil
^ 1 <order> = un <order>
100 1 (mil | <order>) = (ciento un mil | cientoun <order,pl>)
@ (mil | <order>) = %@ (mil | <order,pl>)
"""


def pl_1(order):
    """2, 3, 4"""
    return (order == 'тысяча') and 'тысячи' or order + 'а'

def pl_2(order):
    """5 и больше"""
    return (order == 'тысяча') and 'тысяч' or order + 'ов'

RU_PASSES = """
1 <order> = <order>
2-4 <order> = <order,pl_1>
* <order> = <order,pl_2>
"""

