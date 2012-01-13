# -*- coding: utf-8 -*-
"""A test suite for the listparse module"""

import unittest
from numspell import listparse


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
    "pl_2": lambda x: x == 'millones' and 'millonesa' or '.',
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
    def build_test(self, template, meta=None, good_inputs=[], bad_inputs=[]):
        parser = listparse.Parser(template, meta)

        for list_, result in good_inputs:
            self.assertEqual(result, parser.sub(list_))

        for list_ in bad_inputs:
            self.assertEqual((list_, []), parser.sub(list_))

    def test_phantom(self):
        self.build_test(
            "(1) a (b) (c) = !",
            good_inputs=[
               (['1', 'a', 'b', 'c'], (['1', '!', 'b', 'c'], [(1, 2)])),
            ],
            bad_inputs=[
               ['1', 'a', 'b'],
               ['', 'a', 'b', 'c'],
            ])
    def test_matcher(self):
        self.build_test(
            "<lookup> <order> = {} {}",
            meta=meta,
            good_inputs=[
                (['1', 1], (['un millón'], [(0, 2)])),
                (['.', '21', 2], (['.', 'veintiún billón'], [(1, 3)])),
                (['100', 'mil', '.'], (['cien mil', '.'], [(0, 2)])),
                (['1', 1, '21', 2, '.'],
                 (['un millón', 'veintiún billón', '.'],
                  [(0, 2), (1, 3)])),
            ],
            bad_inputs=[
                ['2', 1],
                ['1', '', 1],
            ])

    def test_modifier(self):
        self.build_test(
            "^ <lookup> <order> = {:pl} {:pl_2}",
            meta=meta,
            good_inputs=[
                (['1', 1], (['un .'], [(0, 2)])),
                (['21', 'mil'], (['veintiún .'], [(0, 2)])),
                (['100', 2, 'etc'], (['cien .', 'etc'], [(0, 2)])),
            ],
            bad_inputs=[
                ['', '1', 1],
                ['21', '1'],
                [' 1 ', 'mil'],
                ['mil', '1'],
            ])

        self.build_test(
            "<lookup> <order> = {0} {1:pl:pl_2}",
            meta=meta,
            good_inputs=[
                (['1', 1], (['un millonesa'], [(0, 2)])),
                (['...', '21', 'mil'],
                 (['...', 'veintiún .'], [(1, 3)])),
                (['.', '1', 'mil', '...', '100', 1, 'etc'],
                 (['.', 'un .', '...', 'cien millonesa', 'etc'],
                  [(1, 3), (3, 5)])),
            ],
            bad_inputs=[
                ['', '1', '', 1],
                ['21', '1'],
                [' 1 ', 'mil'],
                ['mil', '1'],
            ])

        self.build_test(
            "^ x <order> = _ {0} {0:pl} {0:pl:pl_2}",
            meta=meta,
            good_inputs=[
                (['x', 1], (['_ millón millones millonesa'], [(0, 2)])),
                (['x', 'mil'], (['_ mil mil .'], [(0, 2)])),
            ],
            bad_inputs=[
                ['', 'x', 1],
                ['x', '1'],
                [1],
            ])

    def test_combined(self):
        self.build_test(
            "(<gt_1>) <order> <lookup> $ = {:pl} {}",
            meta=meta,
            good_inputs=[
                (['2', 1, '1'], (['2', 'millones un'], [(1, 3)])),
                (['.', '10', 'mil', '21'],
                 (['.', '10', 'mil veintiún'], [(2, 4)])),
            ],
            bad_inputs=[
                ['1', 1, '1'],
                ['2', 1, '1', ''],
            ])

        self.build_test(
            "(1) <order> (<order>) = {:pl:pl_2}",
            meta=meta,
            good_inputs=[
                (['.', '1', 1, 2, '1', 2, 1, '1', 'mil', 'mil', '.'],
                 (['.', '1', 'millonesa', 2, '1', '.', 1, '1', '.', 'mil', '.'],
                  [(2, 3), (5, 6), (8, 9)])),
            ],
            bad_inputs=[
                ['1', 1, '1'],
                ['', '1', 'mil'],
                [1, 1],
            ])


if __name__ == '__main__':
    unittest.main()
