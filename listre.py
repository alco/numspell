"""Regular expressions for lists"""


class ListreObject(object):
    def __init__(self, pattern, meta=None):
        self.pattern = _process_pattern(pattern)
        self.meta = meta or {}

    def match(self, list_):
        return False

    def sub(self, list_):
        return list_


def _process_pattern(pattern):
    return pattern
