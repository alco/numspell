"""A collection of utility functions for the numspell module"""

def isnum(x):
    return type(x) is str and x.isdigit()

def isorder(x):
    return type(x) is int
