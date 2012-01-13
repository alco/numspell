This document describes the syntax of template string used by the **listparse**
module.

## The Basic Structure ##

Template string has the following structure:

    <pattern> = <body>

That is, it consists of two parts--a pattern and a body--with an equals sign
between them.


## The Pattern Syntax ##

The pattern contains a list of tokens separated by whitespace. Each token can
be one of the following:

* one of the special tokens (`^` or `$`)
* a literal token (a simple string with no whitespace)
* a matcher (&lt;matcher_name&gt;)

There are two special tokens. One is _the caret_ (`^`). It can be used in a
pattern only once and only as the first element. It doesn't match any elements
in the list, but it has a special meaning "match only at the beginning of the
list".

The _dolar sign_ (`$`), in a similar manner, is used to match only at the end
of the list. It can only appear once and only at the end of the pattern.

A _matcher_ is a string enclosed in angle brackets (`<` and `>`). The string
itself generally should not contain spaces. For each matcher token in the
pattern there has to be at least one entry in the meta-dictionary which is
passed to the constructor of `Parser`. The key of the entry is built by
appending "~find" to the name of the matcher token. The value is a function
that accepts one argument and returns `True` or `False`. Every time a list
element is matched against the matcher token, the token's "~find" function gets
passed that list element as an argument.


## The Body Syntax

The body is a string with optional substitution tokens. After expanding all of
the tokens (if any) the resulting string replaces the group of list elements
captured by the pattern part of the template, thus becoming a new list element.

A _substitution token_ is similar to that of the Python's format string. In the
simplest case it is written as `{}`. You can include an explicit index like in
`{0}`. If you write index for one of the tokens, every other token must also
have an index (similar to the Python's format string).

Apart from indices, you may also specify _modifiers_ to transform substituted
strings. A modifier is a function which takes one argument (a list element) and
returns a string.


## Pattern Examples ##

    ^ 1 two 'and three' = ...

This pattern consists of four elements.

1. The caret at the beginning signifies that the pattern will match only at the
beginning of a given list.

2. The literal string '1' will match an element '1'.

3. The literal string 'two' will match an element 'two'. The quotes are omitted
in the pattern because neither '1' nor 'two' have spaces in them.

4. The literal string 'and three' will match a corresponding element in a given
list.

This pattern will match the following lists:

    ['1', 'two', 'and three'], ['1', 'two', 'and three', 'bla', bla']

It will not match lists like the following:

    ['...', '1', 'two', 'and three']  # because the special token ^ will match
                                      # only at the beginning of the list

    ['', '1', 'two', 'and three']     # even an empty string or None is still
                                      # considered a list element

**Example 2**.

    (1) <order> = ...

The first element is a phantom element. It will be matched against, but left
intact when it comes to substituting the body of the format string.

The second element is a matcher. For it to work properly, there must be the
"order~find" key in the `meta` dictoinary. The value for the key must be a
function of one argument returning True or False.

If our `meta` dictionary looked like this

    meta = { "order~find": lambda x: type(x) is int }

then the pattern defined above would match the following lists:

    ['1', 2, 'bla'], ['bla', 'bla', '1', 1, 'bla']

It will not, however, match the following lists:

    [1, 2]      # the first element is an integer, not a string '1'
    ['1', '2']  # the second element must be of type int in match against the
                # <order> token



