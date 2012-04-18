"""A collection of utility functions for the numspell module"""

import re


def isnum(x):
    return x and x.isdigit()

def getnum(x):
    return int(x)

def isorder(x):
    return x and re.match('^{\d+}$', x)

def getorder(x):
    """Assumes isorder(x) is True"""
    return int(x[1:-1])

def makeorder(i):
    """type(i) is int"""
    return '{%s}' % i
