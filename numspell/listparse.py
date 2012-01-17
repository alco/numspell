"""List processing based on a simple formatting language

Create an instance of Parser, passing a template string and a substitution
dictionary to the constructor. Then use its 'sub' method to replace groups of
elements of a list with one new element obtained by substituting values of the
elements into the template string.

To learn more about the template string syntax, take a look at the file
TemplateSyntax.md in the 'doc' directory.

"""

__all__ = ['Range', 'Parser']


import re


class Range(object):
    """Encapsulates a range defined by start and end

    'start' stores index of the first matched element in a sequence

    'end' stores index of the element immediately following the last matched
    element in a sequence. In other words, it's the last matched element index
    + 1.

    'span' is a two-element tuple: (start, end).

    """
    def __init__(self, start, length):
        self._start = start
        self._end = start + length
        self._span = (self._start, self._end)

    def _get_start(self):
        return self._start

    def _get_end(self):
        return self._end

    def _get_span(self):
        return self._span

    start = property(_get_start)
    end = property(_get_end)
    span = property(_get_span)


class Parser(object):
    """List processor for element replacement

    Initialize it with a template string and a dictionary which contains
    functions for searching and replacing tokens defined in the template
    string.

    The 'search' method finds the first matching sequence of elements in a
    list.

    The 'sub' method is used to substitute elements in a list.

    """

    def __init__(self, template, meta=None):
        """Initialize the instance with a template string

        Arguments:
          template -- template string

          meta     -- a dictionary with functions needed for searching,
                      replacing and transforming list elements

        """
        pattern_str, body_str = [x.strip() for x in template.split('=')]

        self.meta = meta or {}
        self.pattern = Pattern(pattern_str, self.meta)
        self.body = Body(body_str, self.meta)

    def search(self, list_):
        """Return a Range of the first matching sequence in list_"""
        return self.pattern.search(list_)

    def sub(self, list_):
        """Perform substitution on the given list

        Each sequence of elements matching the pattern defined in the template
        string will be replaced by exactly one element.

        Returns a two-element tuple. The first element is a new list which is
        the result of processing list_. The second element is a list of tuples;
        each tuple stores the range of each sequence of replaced elements.

        """
        result = list_[:]
        ranges = []
        while True:
            m = self.search(result)
            if not m:
                break

            sub_range = (m.start + self.pattern.insets[0],
                         m.end + self.pattern.insets[1])
            result[slice(*sub_range)] = [self.body.format(self.pattern.subs)]
            ranges.append(sub_range)
        return result, ranges


class Pattern(object):
    """Encapsulates a list of tokens for matching"""

    def __init__(self, pattern, meta):
        self.tokens = []        # tokens to match against
        self.subs = []          # substitutions (tokens with values)
        self.offset = 0         # will be set to 1 if pattern has the ^ anchor
        self.insets = (0, 0)    # a bias applied to the range of substitution
        self.length = 0
        self._build(pattern, meta)

    def padded_list(self, index, length):
        """Return a list of tokens padded with None values at the beginning"""
        start_index = max(0, self.offset - index)
        new_list = [None] * (index - self.offset) + self.tokens[start_index:]
        return new_list[:length]

    def search(self, list_):
        """Search for a sequence of elements matching the pattern

        Return a Range of the first sequence of matching elements.

        """
        list_len = len(list_)
        pattern_len = self.length
        if list_len < pattern_len:
            return

        # Run through list_ looking for a matching sequence of elements
        cmp_fn = lambda token, x: (token is None) or token.matches(x)
        for i in range(list_len - pattern_len + 1):
            if all(map(cmp_fn, self.padded_list(i, list_len), list_)):
                return Range(i, pattern_len)

    def _build(self, pattern, meta):
        """Build the 'tokens' and 'subs' lists"""
        elements = re.split(r'\s+', pattern)
        insets = [0, 0]
        left_side = True
        isliteral = lambda token: type(token) is not MatcherToken

        for elem in elements:
            token, isphantom = parse_token(elem, meta)
            if isphantom:
                if left_side:
                    insets[0] += 1
                else:
                    insets[1] -= 1
            elif type(token) is not AnchorToken:
                left_side = False
            self.tokens.append(token)
            if (not isphantom) and (not isliteral(token)):
                self.subs.append(token)

        self.offset = int(elements[0] == '^')
        right_offset = int(elements[-1] == '$')
        self.length = len(self.tokens) - self.offset - right_offset
        self.insets = tuple(insets)


class Body(object):
    """The body defines a replacement for a matching sequence of elements"""
    def __init__(self, body, meta):
        def wrap_fn(wrapper, fn):
            return lambda x: wrapper(fn(x))

        def repl_fn(m):
            fn = lambda token: meta[token.name + "~replace"](token.value)
            wrappers = m.group(1).split(':')
            for w in wrappers[1:]:
                fn = wrap_fn(meta[w], fn)
            self.format_list.append(fn)

            index_str = wrappers[0]
            if index_str:
                index = int(index_str)
            else:
                index = len(self.format_indices)
            self.format_indices.append(index)
            return "{}"

        # Here we look at each substitution token enclosed in { and }. Inside
        # repl_fn, we gather all of the modifiers into a single function using
        # wrap_fn. Then this function is appended to the format_list.
        self.format_list = []
        self.format_indices = []
        self.format_str = re.sub(r'{(.*?)}', repl_fn, body)

    def format(self, tokens):
        """Returns a final string after substituting token values"""
        mapped_tokens = map(lambda i: tokens[i], self.format_indices)
        format_args = [f(x) for f, x in zip(self.format_list, mapped_tokens)]
        return self.format_str.format(*format_args)


class AnchorToken(object):
    """The anchor token allows to match at either end of a list

    This token is represented by ^ and $ symbols in the template string syntax.

    """
    def matches(self, _):
        return False


class LiteralToken(object):
    """Literal token simply matches the string it is given"""
    def __init__(self, string):
        self.string = string

    def matches(self, obj):
        return obj == self.string


class MatcherToken(object):
    """Matcher token uses a function to match against an element

    It also stores the value of the element it matches

    """
    def __init__(self, fn, name):
        self.fn = fn
        self.name = name
        self.value = None

    def matches(self, obj):
        self.value = obj
        return self.fn(obj)


def parse_token(string, meta, phantom=False):
    """Determine the type of the token in string

    Return a tuple with the token and a phantom flag

    """
    # Check for anchors first
    if string in ['^', '$']:
        return AnchorToken(), False

    # Now check for phantoms
    m = re.match(r'^\((.+?)\)$', string)
    if m:
        return parse_token(m.group(1), meta, phantom=True)

    # The rest of tokens
    m = re.match(r'^<(.+?)>$', string)
    if m:
        name = m.group(1)
        fn = meta[name + "~find"]
        token = MatcherToken(fn, name)
    else:
        token = LiteralToken(string)
    return token, phantom
