"""numspell -- a module for spelling integers"""

import logging
import re

import listparse
from squash import squash
from spelling import isnum, isorder


def setup_logging(debug):
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    logging.basicConfig(format="*** %(message)s", level=log_level)

def load_lang_module(lang):
    spelling_mod = "spelling_" + lang
    package = __import__("numspell", fromlist=[spelling_mod])
    return getattr(package, spelling_mod)

def to_list(list_or_str):
    if type(list_or_str) is str:
        return [x.strip() for x in list_or_str.splitlines() if x]
    return list_or_str


class Speller(object):
    """The class which implements the number spelling"""

    def __init__(self, lang="en", debug=False):
        """Initialize the Speller instance with a language code

        Arguments
            lang  -- language code in ISO 639-1 format
            debug -- if True then print debug info to stderr

        """
        setup_logging(debug)

        module = load_lang_module(lang)
        self.RULES = [rule_from_str(x) for x in to_list(module.RULES)]
        self.NUMBERS = module.NUMBERS
        self.ORDERS = module.ORDERS
        if hasattr(module, 'LIST_PASS'):
            self.PASSES = to_list(module.LIST_PASS['passes'])
            self.META = module.LIST_PASS['meta']
        else:
            self.PASSES = []
            self.META = {}

    def spell(self, num):
        """Return the spelling of the given integer

        Arguments:
          num   -- number to spell

        Return value:
          A string with num's spelling.

        """

        if num == 0:
            return self.NUMBERS[0]

        # *** Pass 1. Apply rules to decompose the number ***
        tokens = self._parse_num(num)
        # Renumber orders
        order = 0
        for i in range(len(tokens)-1, -1, -1):
            if isorder(tokens[i]):
                order += 1
                tokens[i] = order
        tokens = squash(isorder, tokens)
        logging.debug("Number decomposition:\n    %s\n", tokens)

        # *** Pass 2. Apply list transformations ***
        processed_tokens = apply_passes(tokens, self.PASSES, self.META)
        for index, token in enumerate(processed_tokens):
            if isnum(token):
                processed_tokens[index] = self.NUMBERS[int(token)]
            elif isorder(token):
                processed_tokens[index] = self.ORDERS[token]
        result = ''.join(processed_tokens).rstrip()

        logging.debug("Final components:\n    %s\n", processed_tokens)

        # Finally, squash any sequence of whitespace into a single space
        return re.sub(r'\s+', ' ', result)

    def check(self, num, spelling):
        """Check if the given spelling is correct

        Arguments:
          num       -- number to spell
          spelling  -- num's spelling

        Return value:
          None if the spelling is correct.
          Otherwise return the correct spelling.

        """
        result = self.spell(num)
        if result == spelling:
            return
        return result

    def _parse_num(self, num):
        """Decompose num into components using self.RULES"""
        if num == 0:
            return []

        numstr = str(num)
        if num in self.NUMBERS:
            return [numstr]

        rule = first_match(numstr, self.RULES)
        body = rule.body.replace('}', '},').replace('{', ',{')
        components = body.split(',')

        logging.debug("Body components:\n    %s", components)

        result = []
        pattern = re.compile(r'{(.+?)}')
        mapping = rule.bind(numstr)
        for raw_token in components:
            match = pattern.match(raw_token)
            if not match:
                result.append(raw_token)
                continue

            token = match.group(1)
            if token == '*':
                result.append(0)
            else:
                new_num = int(''.join(mapping.get(x, x) for x in token))
                result.extend(self._parse_num(new_num))

        return result


def rule_from_str(string):
    """Return a new instance of a rule

    The type of the rule is determined based on the string contents.

    """
    pattern, body = [x.strip() for x in string.split('=')]
    if pattern.find(')') > 0:
        assert pattern.find('(') >= 0
        return RecursiveRule(pattern, body)
    if pattern.find('-') > 0:
        return MultiRule(pattern, body)
    return Rule(pattern, body)


def first_match(numstr, rules):
    """Find the first matching rule for the given number

    This function only looks at the left-hand side of each rule -- the part
    called 'pattern'. The rules are checked in order. The ones which do not
    match the number are discarded.

    For a pattern to match a given number, it must comply with the following
    rules:

      a) if it doesn't contain parentheses:

         * it has the same number of characters (variables or digits) as the
           number has digits
         * each of the its digits (if it has any) has to match exactly with the
           corresponding digits of the number

      b) if it contains parentheses:

         * the number of rightmost characters of the pattern which are not
           enclosed in parentheses must be less than the number of digits in
           the number

    If we end up with no matching rules then the rule-set is not comprehensive
    to cover all possible numbers or there are missing entries in one of the
    lookup tables. Raise an exception and stop further processing.

    """
    for rule in filter(lambda rule: rule.matches(numstr), rules):
        return rule

    raise Exception('Could not find a suitable rule for the number %s' % numstr)

def resolve_bindings(pattern, numstr):
    """Return a dict with variable bindings obtained from numstr"""
    mapping = {}
    for (var, digit) in zip(pattern, numstr):
        if not var.isdigit():
            mapping[var] = mapping.get(var, "") + digit
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

    def bind(self, numstr):
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

    def bind(self, numstr):
        def rsplit_index(s, index):
            return s[:-index], s[len(s)-index:]

        left, right = self.pattern[1:].split(')')
        lnum, rnum = rsplit_index(numstr, len(right))
        mapping = resolve_bindings(right, rnum)
        mapping[left] = lnum
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

    def bind(self, numstr):
        # Clone the leftmost variable a number of times so that the pattern
        # length becomes equal to len(numstr)
        pattern = (self.pattern[0] * (1 + len(numstr) - self.len_range[0])
                   + self.pattern[1:])
        return resolve_bindings(pattern, numstr)


def apply_passes(tokens, passes, meta):
    """Magic processing with index mangling

    Returns a new list with processed tokens.

    """
    # distill tokens into a list of tuples with no whitespace or words
    processed_tokens = [(index, x) for index, x in enumerate(tokens)
                        if isnum(x) or isorder(x)]
    secondary_list = [x for index, x in processed_tokens]
    parts = tokens[:]
    logging.debug("Processed: %s", processed_tokens)
    logging.debug("Secondary: %s", secondary_list)
    logging.debug("Component: %s", parts)

    pass_no = 1
    for pass_ in passes:
        parser = listparse.Parser(pass_, meta)
        new_list, ranges = parser.sub(secondary_list)
        if not ranges:
            continue

        stored_list = secondary_list[:]
        for r in ranges:
            start, end = r
            start_index = processed_tokens[start][0]
            end_index = processed_tokens[end-1][0]

            processed_tokens[start:end] = [(-1, None)]

            subst = [new_list[start]]
            secondary_list[start:end] = subst
            parts[start_index:end_index+1] = subst

            for i in range(start+1, len(processed_tokens)):
                index, token = processed_tokens[i]
                processed_tokens[i] = (index - (end_index - start_index), token)
        logging.debug("Pass #%s:\n    %s\n    -> %s\n    -> %s\n", pass_no, stored_list, pass_, secondary_list)
        pass_no += 1
    if pass_no > 1:
        logging.debug("After final pass:\n    %s\n", parts)

    return parts
