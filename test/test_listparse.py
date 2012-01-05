# -*- coding: utf-8 -*-
"""A test suite for the listparse module"""

import unittest

import listparse


ORDERS = ['', 'millón', 'billón', 'trillón']
NUMBERS = { 2: 'dos', 11: 'once', 90: 'noventa' }

lookup = {
    1: 'un',
    21: 'veintiún',
    100: 'cien',
    }

lr_meta = {
    "_lookup": lookup,

    "order~find": lambda x: type(x) is int or x == 'mil',
    "order~replace": lambda x: x == 'mil' and x or ORDERS[x],

    "lookup~find": lambda x: (type(x) is str) and x.isdigit() and lookup.has_key(int(x)),
    "lookup~replace": lambda x: lookup[int(x)],


    "gt_1~find": lambda x: type(x) is str and x.isdigit() and int(x) > 1,
    "gt_1~replace": lambda x: NUMBERS[int(x)],

    "pl": lambda x: x == 'mil' and 'mil' or x.replace('ón', 'ones'),
    }


class TestLeftAnchor(unittest.TestCase):
    """Patterns starting with ^ should match only at the start of the list
    """

    def setUp(self):
        self.lr = listparse.Parser("^ 1 mil = mil")

    def test_search(self):
        for list_ in [['1', 'mil']]:#, ['1', ' mil'], ['1', ' mil ']]:
            self.assertTrue(self.lr.search(list_))
            self.assertEqual((0, 2), self.lr.search(list_).span)

    def test_not_search(self):
        for list_ in [['10', '1', 'mil'], ['1', '1', 'mil'], ['mil']]:
            self.assertFalse(self.lr.search(list_))


class TestRightAnchor(unittest.TestCase):
    """Patterns ending with $ should match only at the end of the list
    """

    def setUp(self):
        self.lr = listparse.Parser("100 3 $ = hundred and three")

    def test_search(self):
        list_ = ['', '100', '3']
        self.assertTrue(self.lr.search(list_))
        self.assertEqual((1, 3), self.lr.search(list_).span)

    def test_not_search(self):
        for list_ in [['100', '3', 'mil'], ['100', '3', ''], ['100', 1, '3']]:
            self.assertFalse(self.lr.search(list_))

class TestBothAnchors(unittest.TestCase):
    def setUp(self):
        self.lr = listparse.Parser("^ 200 1 <order> $ = ...", lr_meta)

    def test_search(self):
        lr = self.lr
        for list_ in [['200', '1', 2], ['200', '1', 3]]:
            self.assertTrue(lr.search(list_))
            self.assertEqual((0, 3), lr.search(list_).span)

    def test_not_search_1(self):
        self.assertFalse(self.lr.search(['200', '1', 1, '']))

    def test_not_search_2(self):
        self.assertFalse(self.lr.search(['', '200', '1', 2]))

    def test_not_search_3(self):
        self.assertFalse(self.lr.search(['', '200', '1', 2, '']))


class TestOrder(unittest.TestCase):
    """Test order finding and substitution"""

    def setUp(self):
        self.lr = listparse.Parser("^ 1 <order> = un {}", meta=lr_meta)

    def test_anchored_search(self):
        list_ = ['1', 1, 'bla']
        self.assertTrue(self.lr.search(list_))
        self.assertEqual((0, 2), self.lr.search(list_).span)

    def test_normal_search(self):
        lr = listparse.Parser("1 <order> = un {}", meta=lr_meta)
        list_ = ['bla', '1', 2]
        self.assertTrue(lr.search(list_))
        self.assertEqual((1, 3), lr.search(list_).span)

    def test_not_search(self):
        self.assertFalse(self.lr.search(['', '1', 1]))

    def test_sub_sucess(self):
        self.assertEqual(['un billón', 'bla', 'bla'],
                         self.lr.sub(['1', 2, 'bla', 'bla'])[0])

    def test_sub_fail(self):
        self.assertEqual(['', '1', 1, 'bla'], self.lr.sub(['', '1', 1, 'bla'])[0])


class TestConsecutive(unittest.TestCase):
    """Consecutive elements have to search as well"""

    def setUp(self):
        self.lr = listparse.Parser("100 1 mil = ciento un mil")

    def test_search(self):
        list_ = ['bla', '100', '1', 'mil']
        self.assertTrue(self.lr.search(list_))
        self.assertEqual((1, 4), self.lr.search(list_).span)

    def test_not_search(self):
        self.assertFalse(self.lr.search(['100', '', '1', 'mil']))

    def test_sub(self):
        self.assertEqual(['ciento un mil'], self.lr.sub(['100', '1', 'mil'])[0])


class TestAlternative(unittest.TestCase):
    """Alternative searches are handy"""

    def setUp(self):
        self.lr = listparse.Parser("100 1 <order> = "
                                 "ciento un {}",
                                 meta=lr_meta)

    def test_search_1(self):
        list_ = ['bla', '100', '1', 'mil']
        self.assertTrue(self.lr.search(list_))
        self.assertEqual((1, 4), self.lr.search(list_).span)

    def test_search_2(self):
        list_ = ['bla', 'bla', '100', '1', 2]
        self.assertTrue(self.lr.search(list_))
        self.assertEqual((2, 5), self.lr.search(list_).span)

    def test_not_search(self):
        self.assertFalse(self.lr.search(['100', '1', 'ding']))

    def test_sub_1(self):
        self.assertEqual(['bla', 'ciento un mil', 'bla'],
                         self.lr.sub(['bla', '100', '1', 'mil', 'bla'])[0])

    def test_sub_2(self):
        self.assertEqual(['bla', 'ciento un trillón', 'bla'],
                         self.lr.sub(['bla', '100', '1', 3, 'bla'])[0])


class TestAlternative2(unittest.TestCase):
    """This time, only one part of the expression is alternating"""

    def setUp(self):
        self.lr = listparse.Parser("1 <order> = un {}",
                                      meta=lr_meta)

    def test_sub_mil(self):
        self.assertEqual(['un mil'], self.lr.sub(['1', 'mil'])[0])

    def test_sub_millon(self):
        self.assertEqual(['un millón'], self.lr.sub(['1', 1])[0])


class TestModifier(unittest.TestCase):
    """Modifiers are handy"""

    def setUp(self):
        self.lr = listparse.Parser("<gt_1> <order> = {} {:pl}",
                                 meta=lr_meta)

    def test_search(self):
        list_ = ['bla', '2', 1]
        self.assertTrue(self.lr.search(list_))
        self.assertEqual((1, 3), self.lr.search(list_).span)

    def test_not_search(self):
        self.assertFalse(self.lr.search(['1', 1]))

    def test_2(self):
        self.assertEqual(['dos millones'], self.lr.sub(['2', 1])[0])

    def test_11(self):
        self.assertEqual(['once billones'], self.lr.sub(['11', 2])[0])

    def test_90(self):
        self.assertEqual(['noventa trillones'], self.lr.sub(['90', 3])[0])


class TestLookup(unittest.TestCase):
    def setUp(self):
        self.lr = listparse.Parser("<lookup> <order> = {} {:pl}",
                                  meta=lr_meta)

    def test_search(self):
        for key in lr_meta["_lookup"]:
            list_ = [str(key), 1]
            self.assertTrue(self.lr.search(list_))
            self.assertEqual((0, 2), self.lr.search(list_).span)

    def test_not_search(self):
        for num in ['2', '10', '25']:
            self.assertFalse(self.lr.search([num, 1]))

    def test_lookup_1(self):
        self.assertEqual(['un millones'], self.lr.sub(['1', 1])[0])

    def test_lookup_21(self):
        self.assertEqual(['veintiún mil'], self.lr.sub(['21', 'mil'])[0])

    def test_lookup_100_combined(self):
        self.assertEqual(['cien mil', 'cien millones'],
                         self.lr.sub(['100', 'mil', '100', 1])[0])

    def test_lookup_100_1(self):
        self.assertEqual(['cien mil'],
                         self.lr.sub(['100', 'mil'])[0])

    def test_lookup_100_2(self):
        self.assertEqual(['cien millones'],
                         self.lr.sub(['100', 1])[0])


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
        lr = listparse.Parser("^ 1 <order> = {}", ru_meta)

        list_ = ['1', 1]
        self.assertTrue(lr.search(list_))
        self.assertEqual((0, 2), lr.search(list_).span)
        self.assertFalse(lr.search(['', '1', 1]))

        self.assertEqual(['миллион'], lr.sub(['1', 2])[0])
        self.assertEqual(['тысяча'], lr.sub(['1', 1])[0])

    def test_2_to_4(self):
        lr = listparse.Parser("<2_to_4> <order> = {} {:pl_1}", ru_meta)

        self.assertEqual(['два миллиарда'],
                         lr.sub(['2', 3])[0])

        self.assertEqual(['bla', 'четыре миллиона'],
                         lr.sub(['bla', '4', 2])[0])

        self.assertEqual(['bla', 'три тысячи', 'bla'],
                         lr.sub(['bla', '3', 1, 'bla'])[0])

        self.assertEqual(['два миллиарда', 'четыре миллиона', 'два тысячи', 'три триллиона'],
                         lr.sub(['2', 3, '4', 2, '2', 1, '3', 4])[0])

    def test_1_thousand(self):
        lr = listparse.Parser("1 <thousand> = одна тысяча", ru_meta)

        self.assertEqual(['одна тысяча'], lr.sub(['1', 1])[0])

    def test_2_thousand(self):
        lr = listparse.Parser("2 <thousand> = две тысячи", ru_meta)

        self.assertEqual(['две тысячи'], lr.sub(['2', 1])[0])

class TestPhantom(unittest.TestCase):
    def test_simple_phantom(self):
        lr = listparse.Parser("(1) <order> = {}", ru_meta)

        self.assertEqual(['1', 'миллион'], lr.sub(['1', 2])[0])
        self.assertEqual(['whatever', '1', 'миллиард'], lr.sub(['whatever', '1', 3])[0])

    def test_composite_phantom(self):
        lr = listparse.Parser("(<2_to_4>) <order> = {:pl_1}", ru_meta)

        self.assertEqual(['...', '3', 'тысячи'], lr.sub(['...', '3', 1])[0])
        self.assertEqual(['2', 'миллиона'], lr.sub(['2', 2])[0])

if __name__ == '__main__':
    unittest.main(verbosity=2)
