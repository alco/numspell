"""Regular expressions for lists"""

from functools import reduce
from operator import and_
import re


class ListreObject(object):
    def __init__(self, pattern, meta=None):
        self.meta = meta or {}
        self.pattern = _process_pattern(pattern, self.meta)

    def match(self, list_):
        cmp_fun = lambda f, x: f is None or f(x)

        if self.pattern[0] == '^':
            # Match only at the beginning of list_
            blist = map(cmp_fun, self.pattern[1:], list_)
            # Return True if and only if all of the list elements are True
            return reduce(and_, blist)

        list_len = len(list_)
        pat_len = len(self.pattern)
        if list_len < pat_len:
            return False

        for i in range(list_len - pat_len + 1):
            blist = map(cmp_fun, self.pattern, list_[i:])
            if reduce(and_, blist):
                return True

        return False

    def sub(self, list_):
        return list_


def _process_pattern(pattern, meta):
    def make_eq(arg):
        return lambda x: x == arg

    def make_lookup():
        return lambda x: int(x) in meta["_lookup"]

    pat, body = [x.strip() for x in pattern.split('=')]
    pat = re.split(r'\s+', pat)
    for (i, elem) in enumerate(pat):
        if elem == '^':
            assert(i == 0)
            continue

        if elem == '_':
            pat[i] = make_lookup()
        else:
            m = re.match(r'^<(.+?)>$', elem)
            pat[i] = m and meta[m.group(1) + "~find"] or make_eq(elem)

    return pat
