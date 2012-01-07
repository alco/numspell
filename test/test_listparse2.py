# -*- coding: utf-8 -*-
"""A test suite for the listparse module"""

import unittest
from spellnum import listparse


ORDERS = ['', 'millón', 'billón', 'trillón']
NUMBERS = { 2: 'dos', 11: 'once', 90: 'noventa' }

lookup = {
    1: 'un',
    21: 'veintiún',
    100: 'cien',
    }

meta = {
    "order~find": lambda x: type(x) is int or x == 'mil',
    "order~replace": lambda x: x == 'mil' and x or ORDERS[x],

    "lookup~find": lambda x: (type(x) is str) and x.isdigit() and lookup.has_key(int(x)),
    "lookup~replace": lambda x: lookup[int(x)],

    "gt_1~find": lambda x: type(x) is str and x.isdigit() and int(x) > 1,
    "gt_1~replace": lambda x: NUMBERS[int(x)],

    "pl": lambda x: x == 'mil' and 'mil' or x.replace('ón', 'ones'),
    "pl_2": lambda x: x == 'millónes' and 'millonesa' or '.',
    }


class TestSearch(unittest.TestCase):
    def build_test(self, template, meta=None, good_inputs=[], bad_inputs=[]):
        parser = listparse.Parser(template, meta)

        for list_, span in good_inputs:
            self.assertEqual(span, parser.search(list_).span)

        for list_ in bad_inputs:
            self.assertEqual(None, parser.search(list_))

    def test_literal(self):
        self.build_test("a b c d = ",
                        good_inputs=[
                            (['a', 'b', 'c', 'd'], (0, 4)),
                            (['', 'a', 'b', 'c', 'd', 'whatever'], (1, 5)),
                        ],
                        bad_inputs=[
                            ['a', 'b', 'c', 'e'],
                            [],
                            [None],
                            ['whatever'],
                            ['a b c d'],
                        ])

    def test_left_anchor(self):
        self.build_test("^ a = ",
                        good_inputs=[
                            (['a'], (0, 1)),
                            (['a', 'b', '...'], (0, 1)),
                        ],
                        bad_inputs=[
                            ['', 'a', ''],
                            [],
                            [' '],
                            [None, 'a'],
                        ])

    def test_right_anchor(self):
        self.build_test("a b $ = ",
                        good_inputs=[
                            (['a', 'b'], (0, 2)),
                            (['...', 'b', 'a', 'b'], (2, 4)),
                            (['a', 'b', 'a', 'b'], (2, 4)),
                        ],
                        bad_inputs=[
                            ['a', 'b', 'a'],
                            ['a', 'b', 'b'],
                            ['a', 'b', ''],
                            ['...', 'a', 'b', ''],
                        ])

    def test_both_anchors(self):
        self.build_test("^ a b c $ = ",
                        good_inputs=[
                            (['a', 'b', 'c'], (0, 3)),
                        ],
                        bad_inputs=[
                            ['a', ' b ', 'c'],
                            ['', 'a', 'b', 'c'],
                            ['a', 'b', 'c', ''],
                            ['', 'a', 'b', 'c', ''],
                            ['a', 'b', ' ', 'c'],
                            ['a', ' ', 'b', 'c'],
                        ])

    def test_matcher(self):
        self.build_test("<lookup> <order> = ",
                        meta=meta,
                        good_inputs=[
                            (['1', 100], (0, 2)),
                            (['whatever', '21', 'mil'], (1, 3)),
                            (['100', 1, 'blah'], (0, 2)),
                        ],
                        bad_inputs=[
                            ['2', 1],
                            ['', 'mil'],
                        ])
        self.build_test("^ 1 <order> = ",
                        meta=meta,
                        good_inputs=[
                            (['1', 100], (0, 2)),
                            (['1', 'mil'], (0, 2)),
                        ],
                        bad_inputs=[
                            ['', '1', 1],
                            ['', 'mil'],
                            ['1', '100'],
                        ])

    def test_phantom(self):
        self.build_test("(1) (2) check (10) = ",
                        good_inputs=[
                            (['1', '2', 'check', '10'], (0, 4)),
                            (['...', '1', '2', 'check', '10'], (1, 5)),
                            (['1', '2', 'check', '10', 'x'], (0, 4)),
                        ],
                        bad_inputs=[
                            ['check'],
                            ['1', '2', 'check', ' 10 '],
                            [1, 2, 'check', 10],
                        ])

    def test_combined(self):
        self.build_test("^ (1) and <order> $ = ",
                        meta=meta,
                        good_inputs=[
                            (['1', 'and', 1], (0, 3)),
                            (['1', 'and', 'mil'], (0, 3)),
                        ],
                        bad_inputs=[
                            ['1', 'and', '1'],
                            ['', '1', 'and', 10],
                            ['1', 'and', 1, ''],
                            ['x', '1', 'and', 'mil', 'x'],
                        ])


class TestSubstitution(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
