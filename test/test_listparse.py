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

class TestOrder(unittest.TestCase):
    """Test order finding and substitution"""

    def setUp(self):
        self.lr = listparse.Parser("^ 1 <order> = un {}", meta=lr_meta)

    def test_sub_sucess(self):
        self.assertEqual(['un billón', 'bla', 'bla'],
                         self.lr.sub(['1', 2, 'bla', 'bla'])[0])

    def test_sub_fail(self):
        self.assertEqual(['', '1', 1, 'bla'], self.lr.sub(['', '1', 1, 'bla'])[0])


class TestModifier(unittest.TestCase):
    """Modifiers are handy"""

    def setUp(self):
        self.lr = listparse.Parser("<gt_1> <order> = {} {:pl}",
                                 meta=lr_meta)
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
    unittest.main()
