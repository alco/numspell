"""List processing based on a small formatting language

Create an instance of LispObject and then use its `sub` method to replace a
groups of elements of a list with one new element, based on the format string
and the substitution dictionary passed to the instance's constructor.

"""

import re


class MatchObject(object):
    """This class encapsulates the range of matched elements"""

    def __init__(self, start, length):
        """Simply store `start` and calculate `end` and calculate `span`

        Arguments:
            start  -- index of the first elements in the matching sequence
            length -- length of the sequence

        """
        self.start = start
        self.end = start + length - 1
        self.span = (start, self.end)


class LispObject(object):
    """This is a list processor used to perform element replacement

    Initialize it with a format string and a `meta` dictionary which contains
    functions for searching and replacing the tokens mentioned in the format
    string.

    The method for replacing elements in a list is `sub`.

    The `search` method returns a MatchObject containing the range  the format string.

    """

    def __init__(self, format_str, meta=None):
        """Initialize the instance with a format string and a `meta` dictionary

        Arguments:
            format_str -- format string written in the special syntax

            meta       -- dictionary containing functions needed for searching,
                          replacing and transforming list elements

        """
        self.meta = meta or {}
        pattern, body, mapping = _process_string(format_str, self.meta)
        self.pattern, self.body, self.mapping = pattern, body, mapping

    def sub(self, list_):
        """Perform substitution and return a new list along with matches

        Each sequence of elements matching to the pattern defined in the format
        string will be replaced by exactly one element the contents of which is
        based on the format string and the matched elements.

        Return value:
            A two-element tuple. The first element is a new list with the result
            of processing. The second one is a list of `MatchObject`s found
            during processing.

        """
        result = list_[:]
        matches = []
        while True:
            m = self.search(result)
            if not m:
                break
            matches.append(m)

            body = self.body
            for i in range(m.end + 1):
                if i in self.mapping:
                    elem = result[m.start + i]
                    body = body.replace('{%s}' % i, self.mapping[i](elem))
            result[m.start:m.end+1] = [body]

        return result, matches

    def search(self, list_):
        """Search for a sequence of elements matching the format string

        Returns a MatchObject instance encapsulating the range of the first
        sequence of matching elements.

        """
        cmp_fun = lambda f, x: f is None or f(x)
        list_len = len(list_)
        pattern_len = len(self.pattern)

        if self.pattern[0] == '^':
            # Match only at the beginning of list_
            bool_list = map(cmp_fun, self.pattern[1:], list_)
            if list_len >= pattern_len - 1 and all(bool_list):
                return MatchObject(0, pattern_len - 1)
        elif list_len >= pattern_len:
            # Run through the list looking for a matching sequence of elements
            for i in range(list_len - pattern_len + 1):
                bool_list = map(cmp_fun, self.pattern, list_[i:])
                if all(bool_list):
                    return MatchObject(i, pattern_len)
        return None


def _process_string(format_str, meta):
    pattern, body = [x.strip() for x in format_str.split('=')]

    pattern, mapping = _build_pattern(pattern, meta)
    body = _build_body(body, mapping, meta)

    return pattern, body, mapping

def _build_pattern(pattern, meta):
    def make_eq(arg):
        return lambda x: x == arg

    def make_lookup():
        lookup = meta["_lookup"]
        return lambda x: type(x) is str and x.isdigit() and int(x) in lookup

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
            mapping['_'] = i-sub
        else:
            m = re.match(r'^<(.+?)>$', elem)
            if m:
                pat[i] = meta[m.group(1) + "~find"]
                if (m.group(1) + "~replace") in meta:
                    mapping[m.group(1)] = (meta[m.group(1) + "~replace"], i-sub)
            else:
                pat[i] = make_eq(elem)


    return pat, mapping

def _build_body(body, mapping, meta):
    for m in re.finditer(r'<(.+?)>', body):
        comps = [x.strip() for x in m.group(1).split(',')]
        if len(comps) > 1:
            assert(len(comps) == 2)
            f, index = mapping[comps[0]]
            fun = lambda x, g=meta[comps[1]]: g(f(x))
        else:
            fun, index = mapping[m.group(1)]

        body = body.replace(m.group(0), '{%s}' % index)
        mapping[index] = fun

    if '_' in mapping:
        index = mapping['_']
        body = body.replace('_', '{%s}' % index)
        mapping[index] = lambda x: meta["_lookup"][int(x)]

    return body
