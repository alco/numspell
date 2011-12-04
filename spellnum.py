"""A module for spelling integers!
"""

import re
from itertools import ifilter

class Speller(object):
    """The class which performs spelling numbers"""

    def __init__(self, lang="en", rules=None,
                 number_table=None, order_table=None,
                 order_separator=None):
        """Initialize the Speller instance with language code and other options

        lang -- language code in the ISO 639-1 format

        """
        module = __import__("spelling_" + lang)
        self.RULES = [_Rule(x) for x in (rules or module.RULES)]
        self.NUMBERS = number_table or module.NUMBERS
        self.ORDERS = order_table or module.ORDERS
        if order_separator:
            self.ORDER_SEP = order_separator
        elif hasattr(module, 'ORDER_SEP'):
            self.ORDER_SEP = module.ORDER_SEP
        else:
            self.ORDER_SEP = " "

    def spell(self, num):
        """Return the spelling of the given integer

        num   -- the number to spell
        order -- specifies the power of 1000 which is appended to the number

        """

        if int(num) == 0:
            return self.NUMBERS[0]

        result = self._parse_num(str(num))

        # Squash all sequences of ints separated by whitespace leaving only the
        # leftmost number in the sequence.
        for m in re.finditer(r'(\d)\s*(\d\s+)*\d', result):
            result = result[:m.start()] + m.group(1) + result[m.end():]

        # Substitute order names in place of the remaining ints.
        for m in re.finditer(r'\d', result):
            result = result.replace(m.group(0), self.ORDERS[int(m.group(0))])

        return result

    def _parse_num(self, numstr, order=0):
        num = int(numstr)
        if num == 0:
            return ""
        if num in self.NUMBERS:
            result = self.NUMBERS[num]
        else:
            rule = _first_match(numstr, self.RULES)
            mapping = _pattern_match(rule.pattern, numstr, order)
            result = _expand_body(rule.body, mapping, self._parse_num).rstrip()

        if order:
            return (result + self.ORDER_SEP + str(order))
        return result


def _expand_body(body, mapping, callback):
    """Produce a spelling given a rule and a mapping of its vars"""
    result = body
    for raw_token in re.findall(r'{.+?}', body):
        token = raw_token[1:-1]
        order = 0
        for char in token:
            subst = mapping.get(char, char)
            if type(subst) == list:
                subst, order = subst
            token = token.replace(char, str(subst))
        result = result.replace(raw_token, callback(token, order))
    return result

def _first_match(numstr, rules):
    """Find the first matching rule for the given number

    This function only looks at the left-hand side of each rule -- the part
    called 'pattern'. The rules are checked in order. The ones which do not
    match the number are discarded.

    For a pattern to match a given number, it must comply with
    the following rules:

      a) if it doesn't cotain parentheses:

         * it has the same number of characters (variables or digits) as the
           number has digits
         * each of the its digits (if it has any) has to match exactly with the
           corresponding digits of the number

      b) if it contains parentheses:

         * the number of rightmost characters of the pattern which are not
           enclosed in parentheses must be less than the number of digits in the
           number

    IF we end up with no matching rules then the rule set is not comprehensive
    to cover all possible numbers or there are missing entries in one of the
    lookup tables. Raise an exception and stop further processing.

    """
    for rule in ifilter(lambda rule: rule.matches(numstr), rules):
        return rule

    raise Exception('Caould not find a suitable rule for the number %s' % numstr)

def _pattern_match(pattern, numstr, order):
    """Return a mapping for variables given the numstr"""

    def rsplit_index(s, index):
        return s[:-index], s[len(s)-index:]

    mapping = {}
    if pattern.find(')') > 0:
        left, right = pattern[1:].split(')')  # deconstruct the pattern '(a)xxx'
        lnum, rnum = rsplit_index(numstr, len(right))
        mapping[left] = [lnum, order+1]
        mapping.update(_pattern_match(right, rnum, order))
    else:
        for (var, digit) in zip(pattern, numstr):
            mapping[var] = mapping.get(var, 0) * 10 + int(digit)
    return mapping


class _Rule(object):
    def __init__(self, rulestr):
        def _split_rule(rule):
            """Split the given rule into two parts and return a list"""
            return [x.strip() for x in re.split(r'\s*=\s*', rule)]

        self.pattern, self.body = _split_rule(rulestr)

        # Rules with parantheses in their pattern will be treated specially
        # later on.
        self.special = (self.pattern.find(')') > 0)

    def matches(self, num):
        if self.special:
            return self._chopped_len() < len(num)
        if len(self.pattern) == len(num):
            return self._compare_digits(num)

    def _compare_digits(self, num):
        for (char, digit) in zip(self.pattern, num):
            if char.isdigit() and char != digit:
                return False
        return True

    def _chopped_len(self):
        assert(self.special)
        return len(self.pattern) - self.pattern.rindex(')') - 1

# END OF MODULE


def _main_cli(args):
    speller = Speller()
    print speller.spell(args[0])

def _main_test():
    import subprocess

    subprocess.call(['python', 'test.py'])

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1 or sys.argv[1] == '-t':
        _main_test()
    else:
        _main_cli(sys.argv[1:])
