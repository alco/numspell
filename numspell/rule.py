def from_str(string):
    """Return a new instance of the rule encoded in `string`"""
    pattern, body = [x.strip() for x in string.split('=')]
    if pattern.find(')') > 0:
        assert pattern.find('(') >= 0
        return RecursiveRule(pattern, body)
    if pattern.find('-') > 0:
        return MultiRule(pattern, body)
    return Rule(pattern, body)

def resolve_bindings(pattern, numstr):
    """Return a dict with variable bindings obtained from numstr"""
    mapping = {}
    for (var, digit) in zip(pattern, numstr):
        if not var.isdigit():
            mapping[var] = mapping.get(var, "") + digit
    return mapping

class Rule(object):
    """The base class for all rule types

    Implements common functionality such as matching against a number and
    binding variables from a number.

    """

    def __init__(self, pattern, body):
        """Both `pattern` and `body` are strings"""
        self.pattern = pattern
        self.body = body

    def matches(self, numstr):
        """True if the rule's pattern matches `numstr`"""
        assert type(numstr) is str

        return len(self.pattern) == len(numstr) and self._compare_digits(numstr)

    def bind(self, numstr):
        """Return a dict with variable bindings based on `numstr`"""
        assert type(numstr) is str

        return resolve_bindings(self.pattern, numstr)

    def _compare_digits(self, numstr):
        """True if all digits in `numstr` are equal to corresponding digits in the rule's pattern"""
        assert type(numstr) is str

        for (char, digit) in zip(self.pattern, numstr):
            if char.isdigit() and char != digit:
                return False
        return True


class RecursiveRule(Rule):
    """A rule is called recursive if its pattern contains parentheses

    This type of rule cannot contain digits in the pattern

    """

    def matches(self, numstr):
        return self._chopped_len() < len(numstr)

    def bind(self, numstr):
        def rsplit_at(s, index):
            return s[:-index], s[len(s)-index:]

        # left = the part inside the parens
        # right = everything else
        left, right = self.pattern[1:].split(')')
        # lnum is the digit corresponding to the paren variable
        # rnum is the remaining part that'll get bound to variables in `right`
        lnum, rnum = rsplit_at(numstr, len(right))
        mapping = resolve_bindings(right, rnum)
        mapping[left] = lnum
        return mapping

    def _chopped_len(self):
        """The length of the part outside of the parens"""
        return len(self.pattern) - self.pattern.rindex(')') - 1


class MultiRule(Rule):
    """A rule is called a multi-rule if its pattern has at least one dash

    An example from es.spelling:

        a--xxx = {a} {1000} {x}

    This one rule is equivalent to a set of three rules:

        axxx = {a} {1000} {x}
        aaxxx = {a} {1000} {x}
        aaaxxx = {a} {1000} {x}

    """

    def __init__(self, pattern, body):
        Rule.__init__(self, pattern, body)
        dash_count = pattern.count('-')
        self.len_range = range(len(pattern) - dash_count, len(pattern) + 1)
        self.pattern = pattern.replace('-', '')

    def matches(self, numstr):
        return len(numstr) in self.len_range and self._compare_digits(numstr)

    def bind(self, numstr):
        # Clone the leftmost variable a number of times so that the pattern
        # length becomes equal to len(numstr)
        pattern = (self.pattern[0] * (1 + len(numstr) - self.len_range[0])
                   + self.pattern[1:])
        return resolve_bindings(pattern, numstr)

