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

        if hasattr(module, 'PREORDERS'):
            self.PREORDERS = module.PREORDERS
        else:
            self.PREORDERS = {}

    def spell(self, num):
        """Return the spelling of the given integer

        num   -- the number to spell
        order -- specifies the power of 1000 which is appended to the number

        """

        if num == 0:
            return self.NUMBERS[0]

        tokens = self._parse_num(str(num))
        parts = []

        isnum = lambda x: type(x) is str and x.isdigit()
        isorder = lambda x: type(x) is int

        last_significant_thing = None
        for (i, token) in enumerate(tokens):
            part = None
            if isnum(token):
                part = self.NUMBERS[int(token)]
                last_significant_thing = token
            elif isorder(token):
                if not isorder(last_significant_thing):
                    if i > 0 and isnum(tokens[i-1]):
                        if int(tokens[i-1]) in self.PREORDERS:
                            parts[i-1] = self.PREORDERS[int(tokens[i-1])]
                        sep = self.ORDER_SEP
                    else:
                        sep = ''
                    part = sep + self.ORDERS[token]
                    last_significant_thing = token
            else:
                part = token
            if part:
                parts.append(part)

        result = ''.join(parts).rstrip()
        print tokens
        print parts

        return result

    def _parse_num(self, numstr, order=0):
        num = int(numstr)
        if num == 0:
            return ""

        if num in self.NUMBERS:
            result = [numstr]
        else:
            rule = _first_match(numstr, self.RULES)
            mapping = _pattern_match(rule.pattern, numstr, order)
            result = _expand_body(rule.body, mapping, self._parse_num)

        return result + (order and [order] or [])

def _expand_body(body, mapping, callback):
    """Produce a spelling given a rule and a mapping of its vars"""
    print mapping
    body = body.replace('}', '!}')

    result = []
    for item in body.split('{'):
        result.extend(item.split('}'))
    result = filter(bool, result)

    for raw_token in filter(lambda x: x.find('!') > 0, result):
        token = raw_token[:-1]
        order = 0
        for char in token:
            subst = mapping.get(char, char)
            if type(subst) is list:
                subst, order = subst
            token = token.replace(char, str(subst))
        index = result.index(raw_token)
        spelling = callback(token, order)
        if spelling:
            print result
            print spelling
            print '***'
            result = result[:index] + spelling + result[index+1:]
        else:
            result.pop(index)

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


def _run_tests():
    import subprocess
    subprocess.call(['python', 'test.py'])

def _main_cli():
    import argparse

    parser = argparse.ArgumentParser(description='Spell integers in various languages')
    parser.add_argument('num', metavar='number', nargs='?', type=int, help="an integer to spell")
    parser.add_argument('--lang', '-l', type=str, default='en', help="language code in ISO 639-1 format")
    parser.add_argument('--test', '-t', action='store_const', const=True, default=False, help="run unit-tests and exit")
    args = parser.parse_args()

    if args.test or not args.num:
        _run_tests()
        return

    speller = Speller(args.lang)
    print '*%s*' % speller.spell(args.num)

if __name__ == '__main__':
    _main_cli()
