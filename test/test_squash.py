import unittest
from spellnum.squash import squash


def isint(x):
    return type(x) is int


class SquashTest(unittest.TestCase):
    def test_empty_list(self):
        list_ = []
        self.assertEqual(list_, squash(isint, list_))

    def test_one_element(self):
        for list_ in [[1], ['a'], ['None'], '', ' ']:
            self.assertEqual(list_, squash(isint, list_))

    def test_invalid_list(self):
        with self.assertRaises(AssertionError):
            squash(isint, [None])

    def test_no_dupes(self):
        list_ = [1, '2', 3, '4', ' ', 5, '6', ' ', 7, '8', '6', 9]
        self.assertEqual(list_, squash(isint, list_))

    def test_all_dupes(self):
        for list_ in [[1] * 10, [1, '', ' ', ' ', 2, '', 3]]:
            self.assertEqual([1], squash(isint, list_))

    def test_range(self):
        list_ = [' ', '', 1, 2, 3, '', 4, ' ']
        self.assertEqual([' ', '', 1, ' '], squash(isint, list_))

    def test_known_inputs(self):
        known = [
            ([2, 1, 0, 'a'], [2, 'a']),
            (['a', 3, 2, 'b'], ['a', 3, 'b']),
            ([2, 1], [2]),
            (['a', 'b'], ['a', 'b']),
            ([1, 'a', 2, 'b', 3, 4], [1, 'a', 2, 'b', 3]),
        ]
        for given, answer in known:
            self.assertEqual(answer, squash(isint, given))


if __name__ == '__main__':
    unittest.main()
