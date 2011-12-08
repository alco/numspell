"""Regular expressions for lists"""

from functools import reduce
from operator import and_
import re


class MatchObject(object):
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def start(self):
        return self._start

    def end(self):
        return self._end

    def span(self):
        return self._start, self._end


class ListreObject(object):
    def __init__(self, rule, meta=None):
        self.meta = meta or {}
        self.pattern, self.body, self.mapping = _process_rule(rule, self.meta)

    def match(self, list_):
        cmp_fun = lambda f, x: f is None or f(x)

        if self.pattern[0] == '^':
            # Match only at the beginning of list_
            blist = map(cmp_fun, self.pattern[1:], list_)
            # Return a new match object if and only if all of the list elements
            # are True
            if reduce(and_, blist):
                m = MatchObject(0, len(self.pattern) - 2)
                return m
            return None

        list_len = len(list_)
        pat_len = len(self.pattern)
        if list_len < pat_len:
            return None

        for i in range(list_len - pat_len + 1):
            blist = map(cmp_fun, self.pattern, list_[i:])
            if reduce(and_, blist):
                m = MatchObject(i, i + pat_len - 1)
                return m

        return None

    def sub(self, list_):
        m = self.match(list_)
        if not m:
            return list_

        body = self.body
        for i in range(m.end()+1):
            if i in self.mapping:
                elem = list_[m.start() + i]
                body = body.replace('{%s}' % i, self.mapping[i](elem))

        result = list_[:]
        result[m.start():m.end()+1] = [body]
        return result


def _process_rule(rule, meta):
    pattern, body = [x.strip() for x in rule.split('=')]

    pattern, mapping = _build_pattern(pattern, meta)
    body = _build_body(body, mapping)

    return pattern, body, mapping

def _build_pattern(pattern, meta):
    def make_eq(arg):
        return lambda x: x == arg

    def make_lookup():
        return lambda x: int(x) in meta["_lookup"]

    mapping = {}
    pat = re.split(r'\s+', pattern)
    sub = 0
    for (i, elem) in enumerate(pat):
        if elem == '^':
            assert(i == 0)
            sub = 1
            continue

        if elem == '_':
            pat[i] = make_lookup()
        else:
            m = re.match(r'^<(.+?)>$', elem)
            if m:
                pat[i] = meta[m.group(1) + "~find"]
                mapping[m.group(1)] = (meta[m.group(1) + "~replace"], i-sub)
            else:
                pat[i] = make_eq(elem)


    return pat, mapping

def _build_body(body, mapping):
    for m in re.finditer(r'<(.+?)>', body):
        fun, index = mapping[m.group(1)]
        body = body.replace(m.group(0), '{%s}' % index)
        mapping[index] = fun
    return body
