import re
import rule


class Predicate(object):
    def __init__(self, name, value, table):
        self.name = name
        self.value = value
        self.table = table
        self.clauses = []

    def add_clause(self, line):
        self.clauses.append(line)

    def __repr__(self):
        return '<%s: "%s" %s\t%s>' % (self.name, self.value, self.table, self.clauses)


class Modifier(object):
    def __init__(self, name):
        """docstring for __init__"""
        self.name = name
        self.clauses = []

    def add_clause(self, line):
        self.clauses.append(line)

    def __repr__(self):
        return '<%s>' % ([':%s %s' % (self.name, x) for x in self.clauses])


def parse_numbers(lst):
    numbers = {}
    for line in lst:
        num, spelling = line.split(' ', 1)
        numbers[int(num)] = spelling
    return numbers

def parse_orders(lst):
    return lst

def parse_decomp_rules(lst):
    """Create a new Rule instance for each line in `lst`"""
    return [rule.from_str(x) for x in lst]

def parse_transform_rules(lst):
    rules = []
    while len(lst):
        line = lst.pop(0)
        if line == '---':
            break
        rules.append(line)

    NORMAL            = 0
    PARSING_PREDICATE = 1
    PARSING_MODIFIER  = 2

    pred_re = re.compile(r'^(\w+):\s*"(.+)"(?:\s+\*(\w+)\*)?$')
    mod_re = re.compile(r'^:(\w+)$')

    predicates = []
    modifiers = []

    pred = None
    mod = None
    state = NORMAL
    while len(lst):
        line = lst.pop(0)

        match = pred_re.match(line)
        if match:
            state = PARSING_PREDICATE
            pred = Predicate(*match.groups())
            predicates.append(pred)
            continue

        match = mod_re.match(line)
        if match:
            state = PARSING_MODIFIER
            mod = Modifier(match.group(1))
            modifiers.append(mod)
            continue

        if state == PARSING_PREDICATE:
            if line.find('=') > 0:
                pred.add_clause(line)
            else:
                state = NORMAL
        elif state == PARSING_MODIFIER:
            if line.find('=') > 0:
                mod.add_clause(line)
            else:
                state = NORMAL

    print predicates
    print modifiers

    return lst

def parse_user_transform(lst):
    return lst

def parse_section(name, contents):
    if name == 'decompose':
        return parse_decomp_rules(contents)
    if name == 'numbers':
        return parse_numbers(contents)
    if name == 'orders':
        return parse_orders(contents)
    if name == 'transform':
        return parse_transform_rules(contents)
    return parse_user_transform(contents)

def parse_sections(string):
    sections = {}
    section_re = re.compile(r"^\[(\w+)\]$", flags = re.MULTILINE)

    # Get a list of sections, each followed by its contents
    section_list = filter(bool, re.split(section_re, string))
    for i in range(0, len(section_list), 2):
        name = section_list[i]
        contents = [x.strip() for x in section_list[i+1].split('\n')]
        # filter empty lines and comments
        contents = [x for x in contents if x and not x.startswith('%')]
        sections[name] = parse_section(name, contents)
    return sections


if __name__ == '__main__':
    import sys
    with open(sys.argv[1] + '.spelling') as fp:
        config = fp.read()
    print parse_sections(config)
