## The Format String ##

The format string in general looks like this:

    <pattern> = <body>

That is, it consists of two parts--a pattern and a body--with an equals sign
between them.

### The Pattern Syntax ###

The pattern contains a list of tokens separated by whitespace. Each token can be
one of the following:

* one of the special tokens ('^', '$', etc.)
* a regular expression, or a regex literal (r'\s+')
* a matcher (<matcher_name>)

There are two special tokens. The first one is **the caret (^)**. It can be used
in a pattern only once and only as the first element. It doesn't match any
elements in the list, but it has a special meaning "match only at the beginning
of the list".

The **dolar sign ($)**, in a similar manner, is used to match only at the end of
the list. It can only appear once and only at the end of the pattern.

A **matcher** is a string enclosed in angle brackets ('<' and '>'). The string
itself generally should not contain spaces. For each matcher token in the
pattern there has to be at list one corresponding key in the `meta` dictionary
which is passed to the constructor of LispObject. The key is built by append the
string "~find" to the name of the token. See examples below.

### Pattern Examples ###

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



