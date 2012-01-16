The Rule Syntax
===============

The rule syntax is based on pattern matching. Every rule has two parts—a
pattern and a body—separated by an equals sign (`=`). The pattern is matched
against the given number to determine whether the rule is applicable to it.


## The Pattern Syntax ##

The pattern is basically a string of letters and digits. Each letter defines a
variable to store one digit. A variable can be any of the 26 English letters.
When a variable name is repeated several times in succession, that many digits
are stored in it.

Each digit defines a literal match, i.e. in order for any given number to match
a pattern containing digits, every digit in the pattern must be equal to the
corresponding digit (the digit at the same position) of the number.

For instance, given the pattern

    a12xx

trying to match it against the number **11288** would yield the following
bindings:

    a = 1
    x = 88

If we tried to match this pattern against **11000**, we would not get a match
because the number's digit **0** (the third digit from the left) does not equal
to the pattern's corresponding digit **2**.


## The Body Syntax ##

The body of a rule defines the decomposition of a given number. It may
recursively invoke pattern matching on the number's components to eventually
divide the number into primitive components. The spelling of each such
component could then be looked up in the spell-table.

When the pattern of a rule has matched the given number, we take that rule and
expand its body. In other words, we determine what values the variables from
the pattern will get and then we substitute those values in place of variables
in the body of the rule.

Every sequence of English letters or digits enclosed within braces (`{` and
`}`) is called an _expansion_. It basically means "take the contents within a
pair of braces and pass it through to the same algorithm", i.e. spell the
number inside those braces.

## Examples ##

Let's take a look at the rule set for the English language.

    ab = {a0}-{b}
    axx = {a} hundred {x}
    (a)xxx = {a} {x}

That's all we need to define an English speller! Well, almost all. Of course,
we will also need a lookup table for the numbers like _one_, _ten_, _twenty_,
etc. But more on this later.

It's time to describe the spelling algorithm. Let's take the number 26.

1. First, we look the number up in the lookup table. In the English case, it's
   not there.

2. Next, we try to match the rules defined for English against the number. The
   rules are matched in order the are written, one at a time. In our case, the
   matching rule is `ab = {a0}-{b}`.

3. After the matching process we have two variables, `a` and `b`, which have
   the values **2** and **6** respectively.

4. We then expand the body of the matching rule by substituting variable values
   in place of the variables themselves. Thus, we obtain the expanded body
   `{20}-{6}`.

5. Since every pair of braces triggers this same algorithm for the number it
   contains, we go back to the step 1 with the number **20**. This time,
   our lookup table contains an entry for the number, so we get back _twenty_
   and put it in the expanded body to obtain `twenty-{6}`. By performing
   similar steps for the second pair of braces we get the final spelling

        twenty-six

---

Remember that using a variable twice (like `x` in the second rule) is just a
syntactic sugar. The second rule could just as well be written as

    abc = {a} hundred {bc}

So, repeating the variable name in the pattern multiple times is a way to say
to the rule parser "I'd like to store these _N_ consecutive digits in the
variable `x` so that I don't need to come up with many variable names and so
that I could save me some typing when writing the body of the rule".

The third rule is tricky. It is a so called _cycling rule_ because it contains
parentheses. It works differently from the ones we have looked at so far.

...
