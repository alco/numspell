# -*- coding: utf-8 -*-
"""Japanese rules and tables for the spellnum module"""

RULES = """
1x = 十{x}
ab = {a}十{b}
1xx = {100}{x}
axx = {a}{100}{x}
axxx = {a}千{x}
(a)xxxx = {a}{x}
"""

NUMBERS = {
    0: '零',
    1: '一',
    2: '二',
    3: '三',
    4: '四',
    5: '五',
    6: '六',
    7: '七',
    8: '八',
    9: '九',
    10: '十',
    100: '百',
}

ORDERS = [
    '',
    '万', '億', 'billón', 'trillón', 'quadrillón',
    'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion',
    'decillion', 'undecillion', 'duodecillion', 'tredecillion',
    'quattuordecillion', 'quindecillion'
]

ORDER_SEP = ''
