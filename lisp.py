"""List processing based on a small formatting language

Create an instance of LispObject, passing a format string and a substitution
dictionary to the constructor. Then use its `sub` method to replace groups of
elements of a list with one new element, based on the format string.

## The Format String ##

The format string in general looks like this:

    <pattern> = <body>

That is, it consists of two parts--a pattern and a body--with an equals sign
between them.

### The Pattern Syntax ###

The pattern contains a list of tokens separated by whitespace. Each token can be
one of the following:

* one of the special tokens ('^', '$', etc.)
* a regular expression, or a regex literal (r'\s+')
* a matcher (<matcher_name>)

There are two special tokens. The first one is **the caret (^)**. It can be used
in a pattern only once and only as the first element. It doesn't match any
elements in the list, but it has a special meaning "match only at the beginning
of the list".

The **dolar sign ($)**, in a similar manner, is used to match only at the end of
the list. It can only appear once and only at the end of the pattern.

A **matcher** is a string enclosed in angle brackets ('<' and '>'). The string
itself generally should not contain spaces. For each matcher token in the
pattern there has to be at list one corresponding key in the `meta` dictionary
which is passed to the constructor of LispObject. The key is built by append the
string "~find" to the name of the token. See examples below.

### Pattern Examples ###

    ^ 1 two 'and three' = ...

This pattern consists of four elements.

1. The caret at the beginning signifies that the pattern will match only at the
beginning of a given list.

2. The literal string '1' will match an element '1'.

3. The literal string 'two' will match an element 'two'. The quotes are omitted
in the pattern because neither '1' nor 'two' have spaces in them.

4. The literal string 'and three' will match a corresponding element in a given
list.

This pattern will match the following lists:

    ['1', 'two', 'and three'], ['1', 'two', 'and three', 'bla', bla']

It will not match lists like the following:

    ['...', '1', 'two', 'and three']  # because the special token ^ will match
                                      # only at the beginning of the list

    ['', '1', 'two', 'and three']     # even an empty string or None is still
                                      # considered a list element

**Example 2**.

    (1) <order> = ...

The first element is a phantom element. It will be matched against, but left
intact when it comes to substituting the body of the format string.

The second element is a matcher. For it to work properly, there must be the
"order~find" key in the `meta` dictoinary. The value for the key must be a
function of one argument returning True or False.

If our `meta` dictionary looked like this

    meta = { "order~find": lambda x: type(x) is int }

then the pattern defined above would match the following lists:

    ['1', 2, 'bla'], ['bla', 'bla', '1', 1, 'bla']

It will not, however, match the following lists:

    [1, 2]      # the first element is an integer, not a string '1'
    ['1', '2']  # the second element must be of type int in match against the
                # <order> token


"""

import re


class MatchObject(object):
    """This class encapsulates the range of matched elements"""

    def __init__(self, start, length):
        """Constructor

        Arguments:
            start  -- index of the first element in the sequence of matched
                      elements

            length -- length of the sequence

        """
        self.start = start
        self.end = start + length - 1
        self.span = (start, self.end)


class LispObject(object):
    """List processor for element replacement

    Initialize it with a format string and a `meta` dictionary which contains
    functions for searching and replacing tokens mentioned in the format string.

    The `sub` method is used for element replcement in a given list. The
    `search` method checks whether there is a matching sequence of elements in a
    list.

    """

    def __init__(self, format_str, meta=None):
        """Initialize the instance with a format string and a `meta` dictionary

        Arguments:
            format_str -- format string written in the special syntax

            meta       -- dictionary containing functions needed for searching,
                          replacing and transforming list elements

        """
        self.meta = meta or {}

        pattern_str, body_str = [x.strip() for x in format_str.split('=')]
        self.pattern = PatternObject(pattern_str, self.meta)
        self.body = BodyObject(body_str, self.meta)

    def sub(self, list_):
        return self.pattern.sub(list_, self.body)

    def search(self, list_):
        return self.pattern.search(list_)


class BodyObject(object):
    def __init__(self, body, meta):
        def wrap_fn(wrapper, fn):
            return lambda x: wrapper(fn(x))

        def repl_fn(m):
            fn = lambda token: meta[token.name + "~replace"](token.value)
            wrappers = filter(bool, m.group(1).split(':'))
            for w in wrappers:
                fn = wrap_fn(meta[w], fn)
            self.format_list.append(fn)
            return "{}"

        self.format_list = []
        self.format_str = re.sub(r'{(.*?)}', repl_fn, body)

    def formatted_string(self, tokens):
        format_args = [f(x) for f, x in zip(self.format_list, tokens)]
        return self.format_str.format(*format_args)


class AnchorToken(object):
    def matches(self, obj):
        return False


class LiteralToken(object):
    def __init__(self, string):
        self.string = string

    def matches(self, obj):
        return obj == self.string


class MatcherToken(object):
    def __init__(self, fn, name):
        self.fn = fn
        self.name = name
        self.value = None

    def matches(self, obj):
        self.value = obj
        return self.fn(obj)


def isliteral(token):
    return type(token) is not MatcherToken


class PatternObject(object):
    """Encapsulates a list of tokens for matching"""

    def __init__(self, pattern, meta):
        self.tokens = []
        self.left_anchor = False
        self.right_anchor = False
        self.offset = 0
        self.substitutions = []
        self._build(pattern, meta)


    def token_list(self, index):
        return [None] * (index - self.offset) + self.tokens

    def search(self, list_):
        """Search for a sequence of elements matching the format string

        Return a MatchObject instance encapsulating the range of the first
        sequence of matching elements.

        """
        list_len = len(list_)
        pattern_len = len(self.tokens)
        if list_len < pattern_len:
            return None

        def match_from_index(index):
            cmp_fn = lambda token, x: (token is None) or token.matches(x)
            if all(map(cmp_fn, self.token_list(index), list_)):
                return MatchObject(index, pattern_len)

        if self.left_anchor:
            # Match only at the beginning of list_
            m = match_from_index(0)
            if self.right_anchor and list_len != pattern_len:
                return None
            return m

        if self.right_anchor:
            # Match only at the end of list_
            start_index = list_len - pattern_len
            return match_from_index(start_index)

        # Run through list_ looking for a matching sequence of elements
        for i in range(list_len - pattern_len + 1):
            m = match_from_index(i)
            if m:
                return m

    def sub(self, list_, body):
        """Perform substitution and return a new list along with matches

        Each sequence of elements matching the pattern defined in the format
        string will be replaced by exactly one element the contents of which is
        based on the format string and the matched elements.

        Return value: a two-element tuple. The first element is a new list with
        the result of processing. The second one is a list of MatchObject
        instances found during processing.

        """
        result = list_[:]
        matches = []
        while True:
            m = self.search(result)
            if not m:
                break
            matches.append(m)

            span = slice(m.start + self.span[0],
                         m.end + self.span[1] + 1)
            result[span] = [body.formatted_string(self.substitutions)]

        return result, matches


    def _build(self, pattern, meta):
        elements = re.split(r'\s+', pattern)
        span = [0, 0]
        self.left_anchor = (elements[0] == '^')
        self.right_anchor = (elements[-1] == '$')
        if self.left_anchor:
            elements.pop(0)
        if self.right_anchor:
            elements.pop()
        assert '^' not in elements, ("The ^ anchor may only appear as the first"
                                     " token in a pattern")
        assert '$' not in elements, ("The $ anchor may only appear"
                                     " as the last token in a pattern")

        for (i, elem) in enumerate(elements):
            token, isphantom = _parse_token(elem, meta)
            if isphantom:
                if len(self.tokens) == 0:
                    span[0] += 1
                else:
                    span[1] -= 1
            self.tokens.append(token)
            if (not isphantom) and (not isliteral(token)):
                self.substitutions.append(token)
        self.span = tuple(span)


def _parse_token(string, meta, phantom=False):
    """Determine the type of the token in string

    Return value: a 2-tuple with the token and a phantom flag

    """
    m = re.match(r'^\((.+?)\)$', string)
    if m:
        return _parse_token(m.group(1), meta, phantom=True)

    m = re.match(r'^<(.+?)>$', string)
    if m:
        name = m.group(1)
        fn = meta[name + "~find"]
        token = MatcherToken(fn, name)
    else:
        token = LiteralToken(string)
    return token, phantom
