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
    30000: 'treinta mil',
    90000: 'noventa mil',

    100000: 'cien mil',
    200100: 'doscientos mil ciento',
    250000: 'doscientos cincuenta mil',
    934756: 'novecientos treinta y cuatro mil setecientos cincuenta y seis',

    1000000: 'un millón',
    1100234: 'un millón ciento mil doscientos treinta y cuatro',
    6000000: 'seis millones',
    10000000: 'diez millones',
    10678456: 'diez millones seiscientos setenta y ocho mil cuatrocientos cincuenta y seis',
    100000000: 'cien millones',
    300873678: 'trescientos millones ochocientos setenta y tres mil seiscientos setenta y ocho',
    15789513: 'quince millones setecientos ochenta y nueve mil quinientos trece',
    143000000: 'ciento cuarenta y tres millones',
    143007000: 'ciento cuarenta y tres millones siete mil',

    1000000000: 'mil millones',
    10000000000: 'diez mil millones',
    100000000000: 'cien mil millones',
    1000000000000: 'billón',
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
