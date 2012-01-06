__all__ = ['squash']


from operator import add, eq


def squash(predicate, list_):
    """Squash multiple consecutive list elements into one

    For each sequence of elements, optionally interspersed with whitespace or
    empty strings, for which the predicate returns True, leave the first
    element in the sequence and drop the rest.

    Arguments:
      predicate -- function of one argument returning True for squashable
                   elements

      list_     -- list of elements to modify. Every list element, for which
                   the predicate returns False, must be a string.

    Return value:
      A new list with squashed elements. The input list remains unchanged.

    """

    assert not filter(lambda x: not (predicate(x) or type(x) is str), list_)

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
