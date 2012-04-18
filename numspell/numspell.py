"""numspell -- a module for spelling integers"""

import logging
import re

import listparse
import spelling_parser
from squash import squash, squash_whitespace
from spelling import isnum, getnum, isorder, getorder, makeorder


def setup_logging(debug):
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    logging.basicConfig(format="*** %(message)s", level=log_level)

def load_lang_module(lang):
    with open('numspell/lang/%s.spelling' % lang) as fp:
        spell_conf = fp.read()
    return spelling_parser.parse_sections(spell_conf)


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
        self.RULES = module["decompose"]
        self.NUMBERS = module["numbers"]
        self.ORDERS = module["orders"]

        # populate lang_module.predicates with globally available preds
        self.lang_module = module
        if 'transform' in self.lang_module:
            self.lang_module['transform']['predicates']['order'] = spelling_parser.Predicate('order', r'{(\d+)}', self.ORDERS)

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
            if type(tokens[i]) is int:
                tokens[i] = makeorder(order)
                order += 1

        # Squash adjacent orders leaving only the highest one
        tokens = squash(isorder, tokens)
        # Squash adjacent whitespace
        tokens = squash_whitespace(tokens)

        logging.debug("Number decomposition:\n    %s\n", tokens)

        # *** Pass 2. Apply list transformations ***
        if 'transform' in self.lang_module:
            processed_tokens = apply_passes(tokens, self.lang_module['transform'])
        else:
            processed_tokens = tokens

        # Perform final substitution from the NUMBERS and ORDERS tables
        for index, token in enumerate(processed_tokens):
            if isnum(token):
                processed_tokens[index] = self.NUMBERS[getnum(token)]
            elif isorder(token):
                processed_tokens[index] = self.ORDERS[getorder(token)]
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
        """Decompose num into components using RULES for decomposition"""
        if num == 0:
            return []

        numstr = str(num)
        if num in self.NUMBERS:
            return [numstr]

        rule = first_match(numstr, self.RULES)
        components = rule.body.replace('}', '},').replace('{', ',{').split(',')

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
                sub_num = int(''.join(mapping.get(x, x) for x in token))
                result.extend(self._parse_num(sub_num))

        return result


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


def apply_passes(tokens, lang_module):
    """Apply passes one at a time to the list of tokens

    Each token must either be a non-empty string or a space, or an int.

    Returns a new list with processed tokens.

    """
    def merge_tokens(tokens, distilled_tokens):
        """Restores whitespace and punctuation between distilled_tokens

        Null tokens are removed at this stage
        """
        i = 0
        new_tokens = []
        skip_next_whitespace = False
        for index, tok in enumerate(tokens):
            if isnum(tok) or isorder(tok):
                skip_next_whitespace = distilled_tokens[i] is None
                if not skip_next_whitespace:
                    new_tokens.append(distilled_tokens[i])
                i += 1
            elif not skip_next_whitespace:
                new_tokens.append(tok)
        return new_tokens

    # distill tokens into a list of number and order tokens (removing whitespace and punctuation)
    distilled_tokens = [x for x in tokens if isnum(x) or isorder(x)]
    logging.debug("Distilled tokens:\n    %s", distilled_tokens)

    passes = lang_module['rules']
    preds = lang_module['predicates']
    mods = lang_module['modifiers']
    pass_no = 1
    for pass_ in passes:
        parser = listparse.Parser(pass_, preds, mods)
        new_tokens, ranges = parser.sub(distilled_tokens)
        if not len(ranges):
            # List left unchanged
            continue

        assert len(new_tokens) == len(distilled_tokens)

        logging.debug("Pass #%s:\n    %s\n    -> %s\n    -> %s\n",
                        pass_no, distilled_tokens, pass_, new_tokens)
        distilled_tokens = new_tokens
        pass_no += 1

    result = merge_tokens(tokens, distilled_tokens)
    logging.debug("After final pass:\n    %s\n", result)

    return result
