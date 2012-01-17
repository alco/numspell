"""A module for spelling integers!
"""

import re

import listparse
from squash import squash


class Speller(object):
    """The class which performs spelling numbers"""

    def __init__(self, lang="en"):
        """Initialize the Speller instance with language code

        Arguments
            lang -- language code in ISO 639-1 format

        """
        spelling_mod = "spelling_" + lang
        package = __import__("numspell", fromlist=[spelling_mod])
        module = getattr(package, spelling_mod)

        rules = filter(bool, (x.strip() for x in module.RULES.splitlines()))
        self.RULES = [rule_from_str(x) for x in rules]

        self.NUMBERS = module.NUMBERS
        self.ORDERS = module.ORDERS

        if hasattr(module, 'PASSES'):
            self.PASSES = filter(bool,
                                (x.strip() for x in module.PASSES.splitlines()))
        else:
            self.PASSES = []

        self.META = hasattr(module, 'META') and module.META or {}

        if 'order_separator' in self.META:
            self.ORDER_SEP = self.META['order_separator']
        else:
            self.ORDER_SEP = ' '

    def spell(self, num):
        """Return the spelling of the given integer

        Arguments:
          num   -- the number to spell

        Return value:
          A string with the num's spelling.

        """

        if num == 0:
            return self.NUMBERS[0]

        isnum = lambda x: type(x) is str and x.isdigit()
        isorder = lambda x: type(x) is int

        tokens = self._parse_num(str(num))
        ######print '1:', tokens
        # remove multiple sequential orders
        tokens = squash(isorder, tokens)
        ##print '2:', tokens
        # distill tokens into a list of tuples with no whitespace or words
        processed_tokens = [(index, x) for index, x in enumerate(tokens)
                            if isnum(x) or isorder(x)]
        secondary_list = [x for index, x in processed_tokens]
        ##print '        ||'
        ##print '        \/'
        ##print processed_tokens
        ##print secondary_list
        ##print '===='
        parts = tokens[:]

        # prev_token = lambda i, l: l[i-1][1]

        for pass_ in self.PASSES:
            lr = listparse.Parser(pass_, self.META)
            ##print '>>>', pass_
            ##print secondary_list
            ##print lr.search(secondary_list)
            ##print '***---***'
            new_list, matches = lr.sub(secondary_list)
            if not matches:
                continue
            for m in matches:
                ##print 'Processing lists'
                start, end = m
                start_index = processed_tokens[start][0]
                end_index = processed_tokens[end-1][0]

                processed_tokens[start:end] = [(-1, None)]

                subst = [new_list[start]]
                secondary_list[start:end] = subst
                parts[start_index:end_index+1] = subst

                for i in range(start+1, len(processed_tokens)):
                    index, token = processed_tokens[i]
                    processed_tokens[i] = (index - (end_index - start_index), token)

                ##print processed_tokens
                ##print secondary_list
                ##print parts
                ##print '----------------------------'
            ##print secondary_list
            ##print '>>>___<<<'

        for i, (index, token) in enumerate(processed_tokens):
            ##print index, token
            if isnum(token):
                parts[index] = self.NUMBERS[int(token)]
            elif isorder(token):
                parts[index] = self.ORDERS[token]

        ##print parts
        result = ''.join(parts).rstrip()

        # Finally, squash any sequence of whitespace into a single space
        return re.sub(r'\s+', ' ', result)

    def check(self, num, spelling):
        """Check if the given spelling is correct

        Arguments:
          num       -- a number to spell
          spelling  -- num's spelling

        Return value:
          None if the spelling is correct.
          Otherwise return the correct spelling.

        """
        result = self.spell(num)
        if result == spelling:
            return
        return result

    def _parse_num(self, numstr, order=0):
        num = int(numstr)
        if num == 0:
            return ""

        if num in self.NUMBERS:
            result = [numstr]
        else:
            rule = _first_match(numstr, self.RULES)
            mapping = rule.bind(numstr, order)
            result = _expand_body(rule.body, mapping, self._parse_num)

        return result + (order and [self.ORDER_SEP, order] or [])

def _expand_body(body, mapping, callback):
    """Produce a spelling given a rule and a mapping of its vars"""
    ######print mapping
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
            ######print result
            ######print spelling
            ######print '***'
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

      a) if it doesn't contain parentheses:

         * it has the same number of characters (variables or digits) as the
           number has digits
         * each of the its digits (if it has any) has to match exactly with the
           corresponding digits of the number

      b) if it contains parentheses:

         * the number of rightmost characters of the pattern which are not
           enclosed in parentheses must be less than the number of digits in the
           number

    If we end up with no matching rules then the rule-set is not comprehensive
    to cover all possible numbers or there are missing entries in one of the
    lookup tables. Raise an exception and stop further processing.

    """
    for rule in filter(lambda rule: rule.matches(numstr), rules):
        return rule

    raise Exception('Could not find a suitable rule for the number %s' % numstr)


def rule_from_str(string):
    """Return a new instance of a rule

    The type of the rule is determined based on the string contents

    """
    pattern, body = [x.strip() for x in string.split('=')]
    if pattern.find(')') > 0:
        assert pattern.find('(') >= 0
        return RecursiveRule(pattern, body)
    if pattern.find('-') > 0:
        return MultiRule(pattern, body)
    return Rule(pattern, body)

def resolve_bindings(pattern, numstr):
    mapping = {}
    for (var, digit) in zip(pattern, numstr):
        if not var.isdigit():
            mapping[var] = mapping.get(var, 0) * 10 + int(digit)
    return mapping


class Rule(object):
    """The base class for different rule types

    Implements the common functionality for all rule types.

    """

    def __init__(self, pattern, body):
        self.pattern = pattern
        self.body = body

    def matches(self, num):
        """Return True if the rule's pattern matches num"""
        return len(self.pattern) == len(num) and self._compare_digits(num)

    def bind(self, numstr, order):
        """Return a dict with variable bindings"""
        return resolve_bindings(self.pattern, numstr)

    def _compare_digits(self, num):
        for (char, digit) in zip(self.pattern, num):
            if char.isdigit() and char != digit:
                return False
        return True


class RecursiveRule(Rule):
    """A rule is called recursive if its pattern contains parentheses"""

    def matches(self, num):
        return self._chopped_len() < len(num)

    def bind(self, numstr, order):
        def rsplit_index(s, index):
            return s[:-index], s[len(s)-index:]

        left, right = self.pattern[1:].split(')')
        lnum, rnum = rsplit_index(numstr, len(right))
        mapping = resolve_bindings(right, rnum)
        mapping[left] = [lnum, order+1]
        return mapping

    def _chopped_len(self):
        return len(self.pattern) - self.pattern.rindex(')') - 1


class MultiRule(Rule):
    """A rule is called a multi-rule if its pattern has at least one dash"""

    def __init__(self, pattern, body):
        Rule.__init__(self, pattern, body)
        dash_count = pattern.count('-')
        self.len_range = range(len(pattern) - dash_count, len(pattern) + 1)
        self.pattern = pattern.replace('-', '')

    def matches(self, num):
        return len(num) in self.len_range and self._compare_digits(num)

    def bind(self, numstr, order):
        # Clone the leftmost variable a number of times so that the pattern
        # length becomes equal to len(numstr)
        pattern = (self.pattern[0] * (1 + len(numstr) - self.len_range[0])
                   + self.pattern[1:])
        return resolve_bindings(pattern, numstr)
