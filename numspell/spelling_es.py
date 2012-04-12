# -*- coding: utf-8 -*-
"""Spanish rules and tables for the numspell module"""

from spelling import isorder, getorder


RULES = """
ab = {a0} y {b}
axx = {a00} {x}
a--xxx = {a} {1000} {x}
(a)xxxxxx = {a} {*} {x}
"""

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

PASSES = """
^ 1 1000 = mil
^ 1 <order> = un {}
<lookup> (1000) = {}
<lookup> (<order>) = {}
<order> = {:pl}
"""

META = {
    "order~find": isorder,
    "order~replace": lambda x: ORDERS[getorder(x)],
    "lookup~find": lambda x: x in _exceptions,
    "lookup~replace": lambda x: _exceptions[x],
    "pl": lambda x: x.replace('ón', 'ones'),
}

_exceptions = {
    '1': 'un',
    '21': 'veintiún',
    '100': 'cien',
}

LIST_PASS = { 'passes': PASSES, 'meta': META }
