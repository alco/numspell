Template String Syntax
======================

This document describes the template string syntax as defined by the
**listparse** module.


## The Basic Structure ##

Template string has the following structure:

    <pattern> = <body>

That is, it consists of two parts—a pattern and a body—with an equals sign
between them.


## The Pattern Syntax ##

The pattern contains a list of tokens separated by whitespace. Each token can
be one of the following:

* one of the special tokens (`^` or `$`)
* a literal token (a simple string with no whitespace)
* a matcher (&lt;matcher_name&gt;)
* a phantom token (either literal token or a matcher enclosed in parentheses)

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
appending _~find_ to the name of the matcher token. The value is a function
that accepts one argument and returns `True` or `False`. Every time a list
element is matched against the matcher token, the token's _~find_ function gets
passed that list element as an argument.

Lastly, a literal token or a matcher can be enclosed in parentheses (`(` and
`)`) to turn it into a phantom token. A phantom token makes no difference when
matching against the pattern, i.e. `(literal) (<matcher>)` will match the same
sequence as `literal <matcher>` does. However, when it comes to expanding the
body part of the template, phantom tokens are not taken into account like if
they weren't specified at all.


## The Body Syntax

The body is a string with optional substitution tokens. After expanding all of
the tokens (if any) the resulting string replaces the group of list elements
captured by the pattern part of the template, thus becoming a new list element.

A _substitution token_ in the simplest case is written as `{}`. You may specify
an index like in `{0}`. If you specify an index for one of the tokens, every
other token must also have an index (this is similar to the Python's `format`
syntax).

Each substitution token in the body corresponds to one matcher token in the
pattern. Apart from indices, you may also specify _modifiers_ to transform the
string to be substituted. A modifier is a function which takes one argument (a
list element) and returns a string. The modifier name is written after a colon.

A few examples of substitution tokens:

* `{0}`
* `{} {}` (same as `{0} {1}`)
* `{:mod1} {:mod2}` (same as `{0:mod1} {1:mod2}`)
* `{:mod1:mod2}` (same as `{0:mod1:mod2}`)

In the last example two modifiers are combined within one token. Multiple
modifiers are applied from the inside out (or from left to right). That is, the
original string for substitution will be passed as an argument to the `mod1`
function.  Then the return value of `mod1` will be passed to the `mod2`
function. The return value of the latter will replace the whole token in the
final body of the template.

Modifier functions are passed to the parser via the meta-dictionary. For each
modifier there is a dictionary entry with key being the modifier name (like
`mod1` and `mod2` in the examples above) and value being the function itself.


## Examples ##

Let's look at some code to familiarize ourselves with the workings of the
**listparse** module.

```python
from numspell import listparse

ORDERS = ['', 'thousand', 'million']
meta = {
    "gt_1~find": lambda x: (type(x) is str) and x.isdigit() and int(x) > 1,

    "order~find": lambda x: type(x) is int,
    "order~replace": lambda x: ORDERS[x],

    "plural": lambda x: x + "s"
}

parser = listparse.Parser("^ (<gt_1>) <order> = {:plural}", meta=meta)
parser.sub(['2', 1])[0]        # (1)
# ['2', 'thousands']
parser.sub(['10', 2])[0]       # (2)
# ['10', 'millions']
```

Here we use the caret anchor, two matchers, and one modifier.

The caret makes sure that the pattern will match only at the beginning of a
list. So, for example, the list `['', '2', 1]` will not match the pattern.

The first matcher `<gt_1>` is enclosed in parentheses which makes it a phantom
token. It will be matched against, but it won't be replaced during
substitution. That is why we only provide the _gt_1~find_ function without a
complementary _gt_1~replace_ function.

When the substitution token `{:plural}` is expanded, the _order~replace_
function is called first. It gets passed **1** in the case of (1) and **2** in
the case of (2). It returns "thousand" and "million" respectively. Then the
return value is passed to the `plural` modifier to obtain "thousands" for the
first case and "millions" for the second one.

---

Let's look at another example. Assume that we have the same meta-dictionary as
in the example above. We will create a new parser with the following template
string:

```python
parser = listparse.Parser("<order> = {0} {0:plural}", meta=meta)
parser.sub(['a', 1, 'b'])[0]
# ['a', 'thousand thousands', 'b']
```

This time we're using a single matcher in the pattern. Since there are no
anchors, it will match anywhere in a list like the example demonstrates.

In the body of the template we must use explicit indices. Otherwise, the parser
would insert indices automatically and we would end up with an invalid body:
`{0} {1:plural}`. There is only one matcher token, so using the index **1**
would trigger an error.

The actual processing performed to obtain the final result is the same as in
the previous example. The first substitution token (`{0}`) is used as is, while
the second one is transformed by the `plural` modifier.
