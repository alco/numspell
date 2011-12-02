"""Convert an integer number into a string with that number's spelling
"""


import re


class Speller(object):
    """The class which performs spelling numbers"""

    def __init__(self, lang="en",
                 rules=None, number_table=None, order_table=None):
        module = __import__("spelling_" + lang)
        self.RULES = rules or module.RULES
        self.NUMBERS = number_table or module.NUMBERS
        self.ORDERS = order_table or module.ORDERS

    def spell(self, num, order=None):
        """Return the spelling of the given integer number

        num   -- the number to spell
        order -- specifies the power of 1000 which is appended to the number

        """

        num = int(num)  # a simple guard to prevent possible mischief
        if num == 0:
            if order:
                return ""
            return self.NUMBERS[num]

        if order is None:
            order = 0

        spelling = self._parse_num(num)
        if spelling:
            return (spelling.rstrip() + " " + self.ORDERS[order]).rstrip()

        quotient = num / 1000
        assert(quotient > 0)
        remainder = num - quotient * 1000

        left = self.spell(quotient, order+1).rstrip()
        right = self.spell(remainder, order)
        return (left + " " + right).rstrip()

    def _parse_num(self, num):
        if num in self.NUMBERS:
            return self.NUMBERS[num]

        numstr = str(num)
        matching_rule = _best_match(numstr, self.RULES)
        if not matching_rule:
            return None

        pattern, subst = _split_rule(matching_rule)
        mapping = _pattern_match(pattern, numstr)
        return self._expand_rule(subst, mapping)

    def _expand_rule(self, rule, mapping):
        """Produce a spelling given a rule and a mapping of its vars"""
        result = rule
        for raw_token in re.findall('\{.+?\}', rule):
            token = raw_token[1:-1]
            for char in token:
                token = token.replace(char, str(mapping.get(char, char)))
            result = result.replace(raw_token, self.spell(token, 0))
        return result


def _best_match(numstr, rules):
    pattern_len = lambda rule: len(_split_rule(rule)[0])
    candidates = filter(lambda rule: pattern_len(rule) == len(numstr),
                        rules)
    if not candidates:
        return None

    if len(candidates) == 1:
        return candidates[0]
    else:
        print 'CARAMBA'

def _split_rule(rule):
    """Split the given rule into two parts and return a list"""
    return [x.strip() for x in re.split(r'\s*=\s*', rule)]

def _pattern_match(pattern, numstr):
    """Return a mapping for variables given the numstr"""
    mapping = {}
    for (var, digit) in zip(pattern, numstr):
        mapping[var] = mapping.get(var, 0) * 10 + int(digit)
    return mapping


if __name__ == '__main__':
    # rules = filter(lambda x: len(x.strip()), RULE_STRING.split('\n'))
    # for rule in rules:
    #     parts = [x.strip() for x in re.split(r'\s*=\s*', rule)]
    #     pattern = parts[0]
    #     subst = parts[1]
    #     print 'pattern = %s\nsubstitution = %s\n***' % (pattern, subst)

    speller = Speller()
    print '*%s*' % speller.spell(91101001)
