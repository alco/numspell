"""A collection of utility functions for the numspell module"""

def isnum(x):
    return x is not None and x.isdigit()

def getnum(x):
    return int(x)

def isorder(x):
    return x is not None and x.startswith('*') and x[1:-1].isdigit() and x.endswith('*')

def getorder(x):
    """Assumes isorder(x) is True"""
    return int(x[1:-1])

def makeorder(i):
    """type(i) is int"""
    return '*%s*' % i

def isword(x):
    return x is not None and x.startswith('<') and x.endswith('>')

def getword(x):
    return x[1:-1]
