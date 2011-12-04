"""A module for spelling integers!
"""

import re
from itertools import ifilter

class Speller(object):
    """The class which performs spelling numbers"""

    def __init__(self, lang="en",
                 rules=None, number_table=None, order_table=None):
        """Initialize the Speller instance with language code and other options

        lang -- language code in the ISO 639-1 format

        """
        module = __import__("spelling_" + lang)
        self.RULES = [_Rule(x) for x in (rules or module.RULES)]
        self.NUMBERS = number_table or module.NUMBERS
        self.ORDERS = order_table or module.ORDERS

    def spell(self, num):
        """Return the spelling of the given integer

        num   -- the number to spell
        order -- specifies the power of 1000 which is appended to the number

        """
        result = self._parse_num(num)
        for m in re.finditer('(\d)\s+(\d\s+)*\d', result):
            result = result[:m.start()] + m.group(1) + result[m.end():]
        for m in re.finditer('\d', result):
            result = result.replace(m.group(0), self.ORDERS[int(m.group(0))])
        return result

    def _parse_num(self, num, order=None):
        num = int(num)  # a simple guard to prevent possible mischief
        if num == 0:
            if order is None:
                return self.NUMBERS[num]
            return ""

        order = order or 0  # convert None to 0
        numstr = str(num)

        if num in self.NUMBERS:
            spelling = self.NUMBERS[num]
        else:
            matching_rule = _first_match(numstr, self.RULES)
            assert(matching_rule)  # _first_match must throw exception if no rule has matched
            mapping = _pattern_match(matching_rule.pattern, numstr, order)
            spelling = self._expand_body(matching_rule, mapping).rstrip()

        if spelling:
            return (spelling + " " + str(order or self.ORDERS[order])).rstrip()

    def _expand_body(self, rule, mapping):
        """Produce a spelling given a rule and a mapping of its vars"""
        #print mapping
        result = rule.body
        for raw_token in re.findall('{.+?}', rule.body):
            token = raw_token[1:-1]
            order = None
            for char in token:
                subst = mapping.get(char, char)
                if type(subst) == list:
                    order = subst[1]
                    subst = subst[0]
                token = token.replace(char, str(subst))
            result = result.replace(raw_token, self._parse_num(token, order or 0))
        #print result
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


def _main_cli():
    import sys

    speller = Speller()
    print '*%s*' % speller.spell(sys.argv[1])

if __name__ == '__main__':
    _main_cli()
