The Rule Syntax
===============

The rule syntax is based on pattern matching. Every rule has two parts: the
_pattern_ and the _body_, separated by an equals sign (=). The pattern is
matched against the given number to determine whether the rule is applicable
or not in terms of the given number.

Since the best way to learn is to learn by example, let's take a look at the
rule set for the English language.

    ab = {a0}-{b}
    axx = {a} hundred {x}
    (a)xxx = {a} {x}

That's all we need to define an English speller! Well, almost all. Of course,
we will also need a lookup table for the numbers like one, ten, twenty, etc.
But more on this later.

Let's look at the first rule -- `ab = {a0}-{b}`. The part to the left of the
equals sign--the pattern--has two variables: `a` and `b`. A variable is any of
the 26 English letters, each variable can match one and only one digit. So,
the pattern `ab` will match any two-digit number, like 11, 26, 94, and so on.

Now, the pattern of a rule has matched the given number, we take that rule and
expand its body. In other words, we determine what values will the variable
from the pattern will get and then we substitute those values in place of
variable in the body of the rule--the part of the rule to the right of the
equals sign.

Moving on to the rule's body. Every sequence of English letters or digits
enclosed within braces (`{` and `}`) is called an _expansion_. It basically
means "take the contents within a pair of braces and pass it through the same
algorithm", i.e. spell the number inside those braces.

It's time to describe the spelling algorithm. Let's take the number 26.

1. First, we will look the number up in the lookup table. In the case with the
   English language, it's not there.

2. Next, we will try to match the rules defined for English against the
   number. The rules are matched in order the are written, one at a time. In
   our case, the matching rule is `ab = {a0}-{b]`.

3. After the matching process we have two variables, `a` and `b`, which have
   the values `2` and `6`, respectively.

4. We will then expand the body of the matching rule substituting variable
   values in place of the variables themselves. Thus, we obtain the expanded
   body `{20}-{6}`.

5. Since every pair of braces triggers this same algorithm for the number it
   contains, we will go back to the step 1 with the number `20`. This time,
   our lookup table contains an entry for the number, so we get back `twenty`
   and put it in the expanded body to obtain `twenty-{6}`. By performing
   similar steps for the second pair of braces we will finally get the
   spelling, which is

        twenty-six

The only new syntax in the second rule is using the variable `x` twice. This
is just a syntactic sugar. The second rule could just as well be written as

    abc = {a} hundred {bc}

So, repeating the variable name in the pattern multiple times is a way to say
to the rule parser "I'd like to store these _N_ consecutive digits in the
variable `x` so that I don't need to come up with many variable names and so
that I could save me some typing when writing the body of the rule".

The third rule is tricky. It is a so called _cycling rule_ because it contains
parentheses. It works differently from the ones we have looked at before.

...
