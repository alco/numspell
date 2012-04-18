# -*- coding: utf-8 -*-
"""A test suite for the listparse module"""

import unittest
from numspell import listparse
from numspell import spelling_parser



ORDERS = ['', 'millón', 'billón', 'trillón']
NUMBERS = { 2: 'dos', 11: 'once', 90: 'noventa' }

config = """
[decompose]
a = {a}

[numbers]
2 dos
11 once
90 noventa

[orders]
millón
billón
trillón

[transform]
---
lookup: "1|21|100"
  1   = un
  21  = veintiún
  100 = cien

gt_1: "[2-9]|[1-9][0-9]"
  2 = dos
  11 = once
  90 = noventa
---
:pl
  <x>ón = <x>ones

:pl_2
  millones = millonesa
  <x> = .
"""

lang_module = spelling_parser.parse_sections(config)
lang_module['transform']['predicates']['order'] = spelling_parser.Predicate('order', r'{(\d+)}', lang_module['orders'])
lang_module = lang_module['transform']


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
    def build_test(self, template, transform=None, good_inputs=[], bad_inputs=[]):
        transform = transform or {'predicates': {}, 'modifiers': {}}
        parser = listparse.Parser(template, transform['predicates'], transform['modifiers'])

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
                        transform=lang_module,
                        good_inputs=[
                            (['1', '{100}'], (0, 2)),
                            (['whatever', '21', '{0}'], (1, 3)),
                            (['100', '{1}', 'blah'], (0, 2)),
                        ],
                        bad_inputs=[
                            ['2', '{1}'],
                            ['', 'mil'],
                        ])
        self.build_test("^ 1 <order> = ",
                        transform=lang_module,
                        good_inputs=[
                            (['1', '{100}'], (0, 2)),
                        ],
                        bad_inputs=[
                            ['', '1', '{1}'],
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
                            ['{1}', '{2}', 'check', '{10}'],
                        ])

    def test_combined(self):
        self.build_test("^ (1) and <order> $ = ",
                        transform=lang_module,
                        good_inputs=[
                            (['1', 'and', '{1}'], (0, 3)),
                        ],
                        bad_inputs=[
                            ['1', 'and', '1'],
                            ['', '1', 'and', '{10}'],
                            ['1', 'and', '{1}', ''],
                            ['x', '1', 'and', 'mil', 'x'],
                        ])


class TestSubstitution(unittest.TestCase):
    def build_test(self, template, transform=None, good_inputs=[], bad_inputs=[]):
        transform = transform or {'predicates': {}, 'modifiers': {}}
        parser = listparse.Parser(template, transform['predicates'], transform['modifiers'])

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

        self.build_test(
            "(<gt_1>) <order> = {:pl}",
            transform=lang_module,
            good_inputs=[
                (['.', '2', '{0}', '.'], (['.', '2', 'millones', '.'], [(2, 3)])),
                (['10', '{1}'], (['10', 'billones'], [(1, 2)])),
            ],
            bad_inputs=[
                ['1', '{1}'],
                ['0', 'mil'],
            ])

        self.build_test(
            "^ (<gt_1>) <order> = {:pl}",
            transform=lang_module,
            good_inputs=[
                (['2', '{0}'], (['2', 'millones'], [(1, 2)])),
            ],
            bad_inputs=[
                ['', '2', 'mil'],
            ])

    def test_matcher(self):
        self.build_test(
            "<lookup> <order> = {} {}",
            transform=lang_module,
            good_inputs=[
                (['1', '{0}'], ([None, 'un millón'], [(0, 2)])),
                (['.', '21', '{1}'], (['.', None, 'veintiún billón'], [(1, 3)])),
                (['100', '{0}', '.'], ([None, 'cien millón', '.'], [(0, 2)])),
                (['1', '{0}', '21', '{1}', '.'],
                 ([None, 'un millón', None, 'veintiún billón', '.'],
                  [(0, 2), (2, 4)])),
            ],
            bad_inputs=[
                ['2', '{1}'],
                ['1', '', '{1}'],
            ])

    def test_modifier(self):
        self.build_test(
            "^ <lookup> <order> = {:pl} {:pl_2}",
            transform=lang_module,
            good_inputs=[
                (['1', '{1}'], ([None, 'un .'], [(0, 2)])),
                (['21', '{0}'], ([None, 'veintiún .'], [(0, 2)])),
                (['100', '{2}', 'etc'], ([None, 'cien .', 'etc'], [(0, 2)])),
            ],
            bad_inputs=[
                ['', '1', '{1}'],
                ['21', '1'],
                [' 1 ', 'mil'],
                ['mil', '1'],
            ])

        self.build_test(
            "<lookup> <order> = {0} {1:pl:pl_2}",
            transform=lang_module,
            good_inputs=[
                (['1', '{0}'], ([None, 'un millonesa'], [(0, 2)])),
                (['...', '21', '{1}'],
                 (['...', None, 'veintiún .'], [(1, 3)])),
                (['.', '1', '{1}', '...', '100', '{0}', 'etc'],
                 (['.', None, 'un .', '...', None, 'cien millonesa', 'etc'],
                  [(1, 3), (4, 6)])),
            ],
            bad_inputs=[
                ['', '1', '', '{1}'],
                ['21', '1'],
                [' 1 ', 'mil'],
                ['mil', '1'],
            ])

        self.build_test(
            "^ x <order> = _ {0} {0:pl} {0:pl:pl_2}",
            transform=lang_module,
            good_inputs=[
                (['x', '{0}'], ([None, '_ millón millones millonesa'], [(0, 2)])),
            ],
            bad_inputs=[
                ['', 'x', '{1}'],
                ['x', '1'],
                ['{1}'],
            ])

        self.build_test(
            "^ <lookup> <gt_1> <order> = {0} {0:pl_2} {2} {1} {2:pl:pl_2}",
            transform=lang_module,
            good_inputs=[
                (['1', '2', '{0}'], ([None, None, 'un . millón dos millonesa'], [(0, 3)])),
            ])

        self.build_test(
            "^ <lookup> <gt_1> <order> = {1} {2:pl} {0} {0} {2:pl:pl_2}",
            transform=lang_module,
            good_inputs=[
                (['100', '11', '{1}'],
                 ([None, None, 'once billones cien cien .'], [(0, 3)])),
            ])

    def test_combined(self):
        self.build_test(
            "(<gt_1>) <order> <lookup> $ = {:pl} {}",
            transform=lang_module,
            good_inputs=[
                (['2', '{0}', '1'], (['2', None, 'millones un'], [(1, 3)])),
                (['.', '10', '{0}', '21'],
                 (['.', '10', None, 'millones veintiún'], [(2, 4)])),
            ],
            bad_inputs=[
                ['1', '{1}', '1'],
                ['2', '{1}', '1', ''],
            ])

        self.build_test(
            "(1) <order> (<order>) = {:pl:pl_2}",
            transform=lang_module,
            good_inputs=[
                (['.', '1', '{0}', '{2}', '1', '{2}', '{1}', '1', '{1}', '{1}', '.'],
                 (['.', '1', 'millonesa', '{2}', '1', '.', '{1}', '1', '.', '{1}', '.'],
                  [(2, 3), (5, 6), (8, 9)])),
            ],
            bad_inputs=[
                ['1', '{0}', '1'],
                ['', '1', 'mil'],
                ['{0}', '{0}'],
            ])


if __name__ == '__main__':
    unittest.main()
