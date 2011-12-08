# -*- coding: utf-8 -*-
import unittest
import spellnum

english_100 = {
    0: 'zero',
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight',
    9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
    15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty',
    21: 'twenty-one', 22: 'twenty-two', 23: 'twenty-three', 24: 'twenty-four', 25: 'twenty-five',
    26: 'twenty-six', 27: 'twenty-seven', 28: 'twenty-eight', 29: 'twenty-nine', 30: 'thirty',
    31: 'thirty-one', 32: 'thirty-two', 33: 'thirty-three', 34: 'thirty-four', 35: 'thirty-five',
    36: 'thirty-six', 37: 'thirty-seven', 38: 'thirty-eight', 39: 'thirty-nine', 40: 'forty',
    41: 'forty-one', 42: 'forty-two', 43: 'forty-three', 44: 'forty-four', 45: 'forty-five',
    46: 'forty-six', 47: 'forty-seven', 48: 'forty-eight', 49: 'forty-nine', 50: 'fifty',
    51: 'fifty-one', 52: 'fifty-two', 53: 'fifty-three', 54: 'fifty-four', 55: 'fifty-five',
    56: 'fifty-six', 57: 'fifty-seven', 58: 'fifty-eight', 59: 'fifty-nine', 60: 'sixty',
    61: 'sixty-one', 62: 'sixty-two', 63: 'sixty-three', 64: 'sixty-four', 65: 'sixty-five',
    66: 'sixty-six', 67: 'sixty-seven', 68: 'sixty-eight', 69: 'sixty-nine', 70: 'seventy',
    71: 'seventy-one', 72: 'seventy-two', 73: 'seventy-three', 74: 'seventy-four', 75: 'seventy-five',
    76: 'seventy-six', 77: 'seventy-seven', 78: 'seventy-eight', 79: 'seventy-nine', 80: 'eighty',
    81: 'eighty-one', 82: 'eighty-two', 83: 'eighty-three', 84: 'eighty-four', 85: 'eighty-five',
    86: 'eighty-six', 87: 'eighty-seven', 88: 'eighty-eight', 89: 'eighty-nine', 90: 'ninety',
    91: 'ninety-one', 92: 'ninety-two', 93: 'ninety-three', 94: 'ninety-four', 95: 'ninety-five',
    96: 'ninety-six', 97: 'ninety-seven', 98: 'ninety-eight', 99: 'ninety-nine'
}

english_1000 = {
    100: 'one hundred',
    101: 'one hundred one',
    102: 'one hundred two',
    109: 'one hundred nine',
    110: 'one hundred ten',
    120: 'one hundred twenty',
    121: 'one hundred twenty-one',
    198: 'one hundred ninety-eight',
    199: 'one hundred ninety-nine',
    200: 'two hundred',
    203: 'two hundred three',
    204: 'two hundred four',
    211: 'two hundred eleven',
    212: 'two hundred twelve',
    232: 'two hundred thirty-two',
    299: 'two hundred ninety-nine',
    300: 'three hundred',
    400: 'four hundred',
    500: 'five hundred',
    600: 'six hundred',
    700: 'seven hundred',
    800: 'eight hundred',
    900: 'nine hundred',
    999: 'nine hundred ninety-nine'
}

english_infinity = {
    1000: 'one thousand',
    2000: 'two thousand',
    3000: 'three thousand',
    10000: 'ten thousand',
    13000: 'thirteen thousand',
    90000: 'ninety thousand',
    30000: 'thirty thousand',

    1346: 'one thousand three hundred forty-six',
    11482: 'eleven thousand four hundred eighty-two',
    13851: 'thirteen thousand eight hundred fifty-one',
    23016: 'twenty-three thousand sixteen',
    100000: 'one hundred thousand',
    750000: 'seven hundred fifty thousand',
    934756: 'nine hundred thirty-four thousand seven hundred fifty-six',

    1000000: 'one million',
    143000000: 'one hundred forty-three million',
    143007000: 'one hundred forty-three million seven thousand',
    2408701047: 'two billion four hundred eight million seven hundred one thousand forty-seven',
    10680040002031: 'ten trillion six hundred eighty billion forty million two thousand thirty-one'
}

spanish_100 = {
    0: 'cero',
    1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis', 7: 'siete', 8: 'ocho',
    9: 'nueve', 10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce',
    15: 'quince', 16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve', 20: 'veinte',
    21: 'veintiuno', 22: 'veintidós', 23: 'veintitrés', 24: 'veinticuatro', 25: 'veinticinco',
    26: 'veintiséis', 27: 'veintisiete', 28: 'veintiocho', 29: 'veintinueve', 30: 'treinta',
    31: 'treinta y uno', 32: 'treinta y dos', 33: 'treinta y tres', 34: 'treinta y cuatro', 35: 'treinta y cinco',
    36: 'treinta y seis', 37: 'treinta y siete', 38: 'treinta y ocho', 39: 'treinta y nueve', 40: 'cuarenta',
    41: 'cuarenta y uno', 42: 'cuarenta y dos', 43: 'cuarenta y tres', 44: 'cuarenta y cuatro', 45: 'cuarenta y cinco',
    46: 'cuarenta y seis', 47: 'cuarenta y siete', 48: 'cuarenta y ocho', 49: 'cuarenta y nueve', 50: 'cincuenta',
    51: 'cincuenta y uno', 52: 'cincuenta y dos', 53: 'cincuenta y tres', 54: 'cincuenta y cuatro', 55: 'cincuenta y cinco',
    56: 'cincuenta y seis', 57: 'cincuenta y siete', 58: 'cincuenta y ocho', 59: 'cincuenta y nueve', 60: 'sesenta',
    61: 'sesenta y uno', 62: 'sesenta y dos', 63: 'sesenta y tres', 64: 'sesenta y cuatro', 65: 'sesenta y cinco',
    66: 'sesenta y seis', 67: 'sesenta y siete', 68: 'sesenta y ocho', 69: 'sesenta y nueve', 70: 'setenta',
    71: 'setenta y uno', 72: 'setenta y dos', 73: 'setenta y tres', 74: 'setenta y cuatro', 75: 'setenta y cinco',
    76: 'setenta y seis', 77: 'setenta y siete', 78: 'setenta y ocho', 79: 'setenta y nueve', 80: 'ochenta',
    81: 'ochenta y uno', 82: 'ochenta y dos', 83: 'ochenta y tres', 84: 'ochenta y cuatro', 85: 'ochenta y cinco',
    86: 'ochenta y seis', 87: 'ochenta y siete', 88: 'ochenta y ocho', 89: 'ochenta y nueve', 90: 'noventa',
    91: 'noventa y uno', 92: 'noventa y dos', 93: 'noventa y tres', 94: 'noventa y cuatro', 95: 'noventa y cinco',
    96: 'noventa y seis', 97: 'noventa y siete', 98: 'noventa y ocho', 99: 'noventa y nueve'
}

spanish_1000 = {
    100: 'ciento',
    101: 'ciento uno',
    102: 'ciento dos',
    109: 'ciento nueve',
    110: 'ciento diez',
    120: 'ciento veinte',
    121: 'ciento veintiuno',
    130: 'ciento treinta',
    198: 'ciento noventa y ocho',
    199: 'ciento noventa y nueve',
    200: 'doscientos',
    203: 'doscientos tres',
    204: 'doscientos cuatro',
    211: 'doscientos once',
    212: 'doscientos doce',
    232: 'doscientos treinta y dos',
    250: 'doscientos cincuenta',
    299: 'doscientos noventa y nueve',
    300: 'trescientos', 376: 'trescientos setenta y seis',
    400: 'cuatrocientos', 402: 'cuatrocientos dos',
    500: 'quinientos', 515: 'quinientos quince',
    600: 'seiscientos', 611: 'seiscientos once',
    700: 'setecientos', 713: 'setecientos trece',
    800: 'ochocientos', 817: 'ochocientos diecisiete',
    900: 'novecientos', 919: 'novecientos diecinueve',
    999: 'novecientos noventa y nueve'
}

spanish_infinity = {
    1000: 'mil',
    1001: 'mil uno',
    1010: 'mil diez',
    1130: 'mil ciento treinta',
    1134: 'mil ciento treinta y cuatro',
    1345: 'mil trescientos cuarenta y cinco',
    1989: 'mil novecientos ochenta y nueve',
    2000: 'dos mil',
    3000: 'tres mil',
    7456: 'siete mil cuatrocientos cincuenta y seis',
    10000: 'diez mil',
    10567: 'diez mil quinientos sesenta y siete',
    13000: 'trece mil',
    20933: 'veinte mil novecientos treinta y tres',
    21000: 'veintiún mil',
    30000: 'treinta mil',
    90000: 'noventa mil',

    100000: 'cien mil',
    101000: 'ciento un mil',
#    201000: 'doscientos un mil',
#    301000: 'trescientos un mil',
    200100: 'doscientos mil ciento',
    250000: 'doscientos cincuenta mil',
    934756: 'novecientos treinta y cuatro mil setecientos cincuenta y seis',

    1000000: 'un millón',
    1100234: 'un millón cien mil doscientos treinta y cuatro',
    2000000: 'dos millones',
    6000000: 'seis millones',
    21000000: 'veintiún millones',
#    31000000: 'treinta y un millones',

    10000000: 'diez millones',
    10678456: 'diez millones seiscientos setenta y ocho mil cuatrocientos cincuenta y seis',
    100000000: 'cien millones',
    100100000: 'cien millones cien mil',
#    101000000: 'ciento un millones',
    300873678: 'trescientos millones ochocientos setenta y tres mil seiscientos setenta y ocho',
#    301000000: 'trescientos un millones',
    15789513: 'quince millones setecientos ochenta y nueve mil quinientos trece',
    143000000: 'ciento cuarenta y tres millones',
    143007000: 'ciento cuarenta y tres millones siete mil',

    1000000000: 'mil millones',
    2000000000: 'dos mil millones',
    10000000000: 'diez mil millones',
    13000000000: 'trece mil millones',
    21000000000: 'veintiún mil millones',
    100000000000: 'cien mil millones',
#    101000000000: 'ciento un mil millones',
    110000000000: 'ciento diez mil millones',
#    201000000000: 'doscientos un mil millones',
    1000000000000: 'un billón',
}

japanese_100 = {
    0: '零',
    1: '一', 2: '二', 3: '三', 4: '四', 5: '五',
    6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
    11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五',
    16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十',
    21: '二十一', 22: '二十二', 23: '二十三', 24: '二十四', 25: '二十五',
    26: '二十六', 27: '二十七', 28: '二十八', 29: '二十九', 30: '三十',
    31: '三十一', 32: '三十二', 33: '三十三', 34: '三十四', 35: '三十五',
    36: '三十六', 37: '三十七', 38: '三十八', 39: '三十九', 40: '四十',
    41: '四十一', 42: '四十二', 43: '四十三', 44: '四十四', 45: '四十五',
    46: '四十六', 47: '四十七', 48: '四十八', 49: '四十九', 50: '五十',
    51: '五十一', 52: '五十二', 53: '五十三', 54: '五十四', 55: '五十五',
    56: '五十六', 57: '五十七', 58: '五十八', 59: '五十九', 60: '六十',
    61: '六十一', 62: '六十二', 63: '六十三', 64: '六十四', 65: '六十五',
    66: '六十六', 67: '六十七', 68: '六十八', 69: '六十九', 70: '七十',
    71: '七十一', 72: '七十二', 73: '七十三', 74: '七十四', 75: '七十五',
    76: '七十六', 77: '七十七', 78: '七十八', 79: '七十九', 80: '八十',
    81: '八十一', 82: '八十二', 83: '八十三', 84: '八十四', 85: '八十五',
    86: '八十六', 87: '八十七', 88: '八十八', 89: '八十九', 90: '九十',
    91: '九十一', 92: '九十二', 93: '九十三', 94: '九十四', 95: '九十五',
    96: '九十六', 97: '九十七', 98: '九十八', 99: '九十九'
}

japanese_1000 = {
    100: '百',
    101: '百一',
    102: '百二',
    109: '百九',
    110: '百十',
    120: '百二十',
    121: '百二十一',
    198: '百九十八',
    199: '百九十九',
    200: '二百',
    203: '二百三',
    204: '二百四',
    211: '二百十一',
    212: '二百十二',
    232: '二百三十二',
    299: '二百九十九',
    300: '三百',
    400: '四百',
    500: '五百',
    600: '六百',
    700: '七百',
    800: '八百',
    900: '九百',
    999: '九百九十九'
}

japanese_infinity = {
    1000: '一千',
    2000: '二千',
    3000: '三千',
    10000: '一万',
    13000: '一万三千',
    21000: '二万一千',
    90000: '九万',
    30000: '三万',

    1346: '一千三百四十六',
    3481: '三千四百八十一',
    11482: '一万一千四百八十二',
    13851: '一万三千八百五十一',
    23016: '二万三千十六',
    100000: '十万',
    130010: '十三万十',
    750000: '七十五万',
    901102: '九十万一千百二',
    934756: '九十三万四千七百五十六',

    1000000: '百万',
    1200080: '百二十万八十',
    143000000: '一億四千三百万',
    1300000102: '十三億百二',
}


class SharedTest(unittest.TestCase):
    def _run_test(self, answers):
        for num, spelling in sorted(answers.items()):
            self.assertEqual(spelling, self.speller.spell(num))

class EnglishTest(SharedTest):
    def setUp(self):
        self.speller = spellnum.Speller('en')
###
    def test_upto_100(self):
        self._run_test(english_100)

    def test_upto_1000(self):
        self._run_test(english_1000)

    def test_upto_infinity(self):
        self._run_test(english_infinity)


class SpanishTest(SharedTest):
    def setUp(self):
        self.speller = spellnum.Speller('es')

    def test_upto_100(self):
        self._run_test(spanish_100)

    def test_upto_1000(self):
        self._run_test(spanish_1000)

    def test_upto_infinity(self):
        self._run_test(spanish_infinity)

class JapaneseTest(SharedTest):
    def setUp(self):
        self.speller = spellnum.Speller('ja')

    def test_upto_100(self):
        self._run_test(japanese_100)

    def test_upto_1000(self):
        self._run_test(japanese_1000)

    def test_upto_infinity(self):
        self._run_test(japanese_infinity)


if __name__ == '__main__':
    unittest.main(verbosity=2)
