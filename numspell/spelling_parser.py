import re
import rule

class Spelling(object):
    def __init__(self, string):
        self.decomp_rules = parse_decomp_rules(string)
        self.numbers = parse_numbers(string)
        self.orders = parse_orders(string)

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
    section_re = re.compile(r"\[(\w+)\]")

    # Get a list of sections, each followed by its contents
    section_list = filter(bool, re.split(section_re, string))
    for i in range(0, len(section_list), 2):
        name = section_list[i]
        contents = filter(bool, [x.strip() for x in section_list[i+1].split('\n')])
        sections[name] = parse_section(name, contents)
    return sections

if __name__ == '__main__':
    import sys
    with open(sys.argv[1] + '.spelling') as fp:
        config = fp.read()
    print parse_sections(config)
