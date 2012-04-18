import re
import rule


class Clause(object):
    def __init__(self, string):
        """docstring for __init__"""
        left, right = [x.strip() for x in string.split('=')]
        self.pattern = left
        self.body = right

        # 1. Ensure that the pattern contains at most one var
        var_re = re.compile(r'<(\w+?)>')
        assert len(var_re.findall(self.pattern)) <= 1

        # 2. Ensure that if the pattern contains a var, the body
        #    contains the same var
        match = var_re.search(self.pattern)
        if match:
            name = match.group(1)
            assert len(var_re.findall(self.body)) == 1
            assert var_re.search(self.body).group(1) == name
        else:
            assert len(var_re.findall(self.body)) == 0

        self.var_re = var_re

    def match(self, string):
        """Returns a replacement for the string if it matches the pattern

        Otherwise, returns None

        """
        match = self.var_re.search(self.pattern)
        if match:
            # Find out which part of the string should be assigned
            # to the var
            new_pat = self.var_re.sub('(.*)', self.pattern)
            nm = re.match(new_pat, string)
            if nm:
                return self.var_re.sub(nm.group(1), self.body)
        elif string == self.pattern:
            return self.body


class Predicate(object):
    def __init__(self, name, pattern, table):
        self.name = name

        if pattern.find('(') < 0:
            pattern = '(%s)' % pattern
        self.pattern = '^%s$' % pattern
        self.table = table
        self.clauses = []

    def add_clause(self, line):
        clause = Clause(line)
        self.clauses.append(clause)

    def match(self, string):
        if not string:
            return None
        #print 'PATTERN = %s' % self.pattern
        #print '%s MATCH TO %s =' % (self.name, string)
        #print '\t%s' % re.match(self.pattern, string)
        if string:
            return re.match(self.pattern, string)

    def sub(self, string):
        #print 'DID ENTER PREDICATE %s SUB' % self.name
        if self.table:
            match = re.match(self.pattern, string)
            contents = match.group(1)
            return self.table[int(contents)]
        else:
            for clause in self.clauses:
                repl = clause.match(string)
                if repl: return repl

    def __repr__(self):
        return '<%s: "%s" %s\t%s>' % (self.name, self.pattern, self.table, self.clauses)


class Modifier(object):
    def __init__(self, name):
        """docstring for __init__"""
        self.name = name
        self.clauses = []

    def add_clause(self, line):
        clause = Clause(line)
        self.clauses.append(clause)

    def sub(self, string):
        for clause in self.clauses:
            repl = clause.match(string)
            if repl: return repl

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

    pred_re = re.compile(r'^([^:]+):\s*"(.+)"(?:\s+\*(\w+)\*)?$')
    mod_re = re.compile(r'^:(\w+)$')

    predicates = {}
    modifiers = {}

    pred = None
    mod = None
    state = NORMAL
    while len(lst):
        line = lst.pop(0)

        match = pred_re.match(line)
        if match:
            state = PARSING_PREDICATE
            pred = Predicate(*match.groups())
            predicates[pred.name] = pred
            continue

        match = mod_re.match(line)
        if match:
            state = PARSING_MODIFIER
            mod = Modifier(match.group(1))
            modifiers[mod.name] = mod
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

    return {
        'rules': rules,
        'predicates': predicates,
        'modifiers': modifiers
    }

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
