# -*- coding: utf-8 -*-
"""A test suite for listre module"""

import unittest

import listre


ORDERS = ['', 'millón', 'billón', 'trillón']
NUMBERS = { 2: 'dos', 11: 'once', 90: 'noventa' }

lr_meta = {
    "_lookup": {
        1: 'un',
        21: 'veintiún',
        100: 'cien',
        },

    "order~find": lambda x: type(x) is int or x == 'mil',
    "order~replace": lambda x: x == 'mil' and x or ORDERS[x],

    "gt_1~find": lambda x: type(x) is str and x.isdigit() and int(x) > 1,
    "gt_1~replace": lambda x: NUMBERS[int(x)],

    "pl": lambda x: x == 'mil' and 'mil' or x.replace('ón', 'ones'),
    }


class TestAnchors(unittest.TestCase):
    """Patterns starting with ^ should match only at the start of the list
    """

    def setUp(self):
        self.lr = listre.ListreObject("^ 1 mil = mil")

    def test_match(self):
        for list_ in [['1', 'mil']]:#, ['1', ' mil'], ['1', ' mil ']]:
            self.assertTrue(self.lr.match(list_))

    def test_not_match(self):
        for list_ in [['10', '1', 'mil'], ['1', '1', 'mil'], ['mil']]:
            self.assertFalse(self.lr.match(list_))


class TestOrder(unittest.TestCase):
    """Test order finding and substitution"""

    def setUp(self):
        self.lr = listre.ListreObject("^ 1 <order> = un <order>", meta=lr_meta)

    def test_anchored_match(self):
        self.assertTrue(self.lr.match(['1', 1, 'bla']))

    def test_normal_match(self):
        lr = listre.ListreObject("1 <order> = un <order>", meta=lr_meta)
        self.assertTrue(lr.match(['bla', '1', 2]))

    def test_not_match(self):
        self.assertFalse(self.lr.match(['', '1', 1]))

    def test_sub_sucess(self):
        self.assertEqual(['un billón', 'bla', 'bla'],
                         self.lr.sub(['1', 2, 'bla', 'bla']))

    def test_sub_fail(self):
        self.assertEqual(['', '1', 1, 'bla'], self.lr.sub(['', '1', 1, 'bla']))


class TestConsecutive(unittest.TestCase):
    """Consecutive elements have to match as well"""

    def setUp(self):
        self.lr = listre.ListreObject("100 1 mil = ciento un mil")

    def test_match(self):
        self.assertTrue(self.lr.match(['bla', '100', '1', 'mil']))

    def test_not_match(self):
        self.assertFalse(self.lr.match(['100', '', '1', 'mil']))

    def test_sub(self):
        self.assertEqual(['ciento un mil'], self.lr.sub(['100', '1', 'mil']))


class TestAlternative(unittest.TestCase):
    """Alternative matches are handy"""

    def setUp(self):
        self.lr = listre.ListreObject("100 1 <order> = "
                                 "ciento un <order>",
                                 meta=lr_meta)

    def test_match_1(self):
        self.assertTrue(self.lr.match(['bla', '100', '1', 'mil']))

    def test_match_2(self):
        self.assertTrue(self.lr.match(['bla', '100', '1', 2]))

    def test_not_match(self):
        self.assertFalse(self.lr.match(['100', '1', 'ding']))

    def test_sub_1(self):
        self.assertEqual(['bla', 'ciento un mil', 'bla'],
                         self.lr.sub(['bla', '100', '1', 'mil', 'bla']))

    def test_sub_2(self):
        self.assertEqual(['bla', 'ciento un trillón', 'bla'],
                         self.lr.sub(['bla', '100', '1', 3, 'bla']))


class TestAlternative2(unittest.TestCase):
    """This time, only one part of the expression is alternating"""

    def setUp(self):
        self.lr = listre.ListreObject("1 <order> = un <order>",
                                      meta=lr_meta)

    def test_sub_mil(self):
        self.assertEqual(['un mil'], self.lr.sub(['1', 'mil']))

    def test_sub_millon(self):
        self.assertEqual(['un millón'], self.lr.sub(['1', 1]))


class TestModifier(unittest.TestCase):
    """Modifiers are handy"""

    def setUp(self):
        self.lr = listre.ListreObject("<gt_1> <order> = <gt_1> <order,pl>",
                                 meta=lr_meta)

    def test_match(self):
        self.assertTrue(self.lr.match(['bla', '2', 1]))

    def test_not_match(self):
        self.assertFalse(self.lr.match(['1', 1]))

    def test_2(self):
        self.assertEqual(['dos millones'], self.lr.sub(['2', 1]))

    def test_11(self):
        self.assertEqual(['once billones'], self.lr.sub(['11', 2]))

    def test_90(self):
        self.assertEqual(['noventa trillones'], self.lr.sub(['90', 3]))


class TestLookup(unittest.TestCase):
    def setUp(self):
        self.lr = listre.ListreObject("_ <order> = _ <order, pl>",
                                      meta=lr_meta)

    def test_match(self):
        for key in lr_meta["_lookup"]:
            self.assertTrue(self.lr.match([str(key), 1]))

    def test_not_match(self):
        for num in ['2', '10', '25']:
            self.assertFalse(self.lr.match([num, 1]))

    def test_lookup_1(self):
        self.assertEqual(['un millones'], self.lr.sub(['1', 1]))

    def test_lookup_21(self):
        self.assertEqual(['veintiún mil'], self.lr.sub(['21', 'mil']))

    def test_lookup_100_combined(self):
        self.assertEqual(['cien mil', 'cien millones'],
                         self.lr.sub(['100', 'mil', '100', 1]))

    def test_lookup_100_1(self):
        self.assertEqual(['cien mil'],
                         self.lr.sub(['100', 'mil']))

    def test_lookup_100_2(self):
        self.assertEqual(['cien millones'],
                         self.lr.sub(['100', 1]))


RU_ORDERS = ['', 'тысяча', 'миллион', 'миллиард', 'триллион']
RU_NUMBERS = {
    1: 'один',
    2: 'два',

    3: 'три',
    4: 'четыре',
    5: 'пять',
    10: 'десять',
    }

ru_meta = {
    "order~find": lambda x: type(x) is int,
    "order~replace": lambda x: RU_ORDERS[x],

    "thousand~find": lambda x: type(x) is int and x == 1,

    "2_to_4~find": lambda x: type(x) is str and x.isdigit() and 2 <= int(x) <= 4,
    "2_to_4~replace": lambda x: RU_NUMBERS[int(x)],

    "not_1~find": lambda x: type(x) is str and x.isdigit() and int(x) != 1,
    "not_1~replace": lambda x: RU_NUMBERS[int(x)],

    "pl_1": lambda x: (x == 'тысяча') and 'тысячи' or x + 'а',
    "pl_2": lambda x: (x == 'тысяча') and 'тысяч' or x + 'ов',
    }

class TestRussian(unittest.TestCase):
    def test_anchor(self):
        lr = listre.ListreObject("^ 1 <order> = <order>", ru_meta)

        self.assertTrue(lr.match(['1', 1]))
        self.assertFalse(lr.match(['', '1', 1]))

        self.assertEqual(['миллион'], lr.sub(['1', 2]))
        self.assertEqual(['тысяча'], lr.sub(['1', 1]))

    def test_2_to_4(self):
        lr = listre.ListreObject("<2_to_4> <order> = <2_to_4> <order, pl_1>", ru_meta)

        self.assertEqual(['два миллиарда'],
                         lr.sub(['2', 3]))

        self.assertEqual(['bla', 'четыре миллиона'],
                         lr.sub(['bla', '4', 2]))

        self.assertEqual(['bla', 'три тысячи', 'bla'],
                         lr.sub(['bla', '3', 1, 'bla']))

        self.assertEqual(['два миллиарда', 'четыре миллиона', 'два тысячи', 'три триллиона'],
                         lr.sub(['2', 3, '4', 2, '2', 1, '3', 4]))

    def test_1_thousand(self):
        lr = listre.ListreObject("1 <thousand> = одна тысяча", ru_meta)

        self.assertEqual(['одна тысяча'], lr.sub(['1', 1]))

    def test_2_thousand(self):
        lr = listre.ListreObject("2 <thousand> = две тысячи", ru_meta)

        self.assertEqual(['две тысячи'], lr.sub(['2', 1]))

if __name__ == '__main__':
    unittest.main(verbosity=2)
