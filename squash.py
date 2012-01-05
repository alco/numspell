__all__ = ['squash']

from operator import add, eq
import unittest

def squash(predicate, list_):
    """Squash multiple consecutive list elements into one

    For each sequence of elements, optionally interspersed with whitespace or
    empty strings, for which the predicate returns True, leave the first element
    in the sequence and drop the rest.

    Arguments:
      predicate -- function of one argument returning True for squashable
                   elements

      list_     -- list of elements to modify

    Return value:
      A new list with squashed elements. The input list remains unchanged.

    """

    def find(index, list_):
        """Find the first element which satisfies the predicate

        Return the index of the first element in list_[index:] for which
        predicate(elem) is True.

        Return -1 if no such  element has been found.

        """
        indices = [i for i, x in enumerate(list_[index:]) if predicate(x)]
        if indices:
            return index + indices[0]
        return -1

    result = list_[:]
    base = 0
    while True:
        base = find(base, result)
        if base < 0:
            break

        n = find(base+1, result)
        if n < 0:
            break

        if not reduce(add, result[base+1:n], '').strip():
            # There are either no elements or only whitespace and empty string
            # elements between base and n.
            result[base+1:n+1] = []
        else:
            base = n
    return result


### TESTS ###

def isint(x):
    return type(x) is int


class SquashTest(unittest.TestCase):
    def test_empty_list(self):
        list_ = []
        self.assertEqual(list_, squash(isint, list_))

    def test_one_element(self):
        for list_ in [[1], ['a'], [None], '', ' ']:
            self.assertEqual(list_, squash(isint, list_))

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
