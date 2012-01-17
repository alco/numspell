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

Each digit in a pattern defines a literal match, i.e. in order for any given
number to match a pattern containing digits, every digit in the pattern must be
equal to the corresponding digit (the digit at the same position) of the
number.

For instance, given the pattern

    a12xx

trying to match it against the number **11288** would yield the following
bindings

    a = 1
    x = 88

If we tried to match this pattern against **11088**, we would not get a match
because the number's digit **0** (the third digit from the left) differs from
the pattern's corresponding digit **2**.

### Consuming Patterns ###

There is also a way to match against a number with variable number of digits.
This can be achieved by using a _consuming pattern_. When the leftmost variable
of a pattern is enclosed in parentheses (`(` and `)`), the pattern becomes
consuming. It must have at least two variables. The variables outside of
parentheses store the digits as usual, and the rest of the number is stored in
the first variable (the enclosed one), i.e. that variable consumes a part of
the number.

For example, the pattern

    (a)bxx

will match any number with 4 or more digits.

Here are a few examples of matching the pattern against different numbers and
of the resulting variable bindings:

    matching (a)bxx against 1000 yields
      a = 1
      b = 0
      x = 0

    (a)bxx ~ 134081102:
      a = 134081
      b = 1
      x = 2

    (a)bxx ~ 1000100021:
      a = 1000100
      b = 0
      x = 21

Consuming patterns are useful when dealing with numbers starting from 1000 and
up to infinity.

### Multi-patterns ###

In practical use it may be necessary to employ a series of rules with patterns
that differ very little.

Let's write the rules for the Spanish language using the knowledge we have
obtained so far. The body syntax is not important at the moment, it is
explained in the next section.

    ab = {a0} y {b}                (1)
    axx = {a00} {x}                (2)
    axxx = {a} {1000} {x}          (3)
    aaxxx = {a} {1000} {x}         (4)
    aaaxxx = {a} {1000} {x}        (5)
    (a)xxxxxx = {a} {x}            (6)

The patterns of the rules 3—5 look almost the same and their bodies are exactly
the same. There is actually a syntax aimed at eliminating this redundancy. We
can replace the rules 3—5 with a single rule

    a--xxx = {a} {1000} {x}

Speaking more formally, the dash (`-`) in a pattern represents either nothing
or a variable or digit it follows, depending on the number we're trying to
match against.

So, using this piece of syntactic sugar we can rewrite the rules for Spanish in
the following way:

    ab = {a0} y {b}
    axx = {a00} {x}
    a--xxx = {a} {1000} {x}
    (a)xxxxxx = {a} {x}

In this way we end up with 4 rules instead of 6.


## The Body Syntax ##

The body of a rule defines the decomposition of a given number. It may
recursively invoke pattern matching on the number's components to eventually
divide the number into primitive components. The spelling of each component can
then be looked up in the spell-table.

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

Let's take the number **26** and trace the steps needed to obtain its spelling.

1. First, we look the number up in the spell-table. In the English case, it's
   not there.

2. Next, we try to match the number against each of the rules defined for the
   chosen language. The rules are matched in order they are written, one at a
   time. In this case, the matching rule is `ab = {a0}-{b}`.

3. After the matching process we have two variables, `a` and `b`, which have
   the values **2** and **6** respectively.

4. We then expand the body of the matching rule by substituting variable values
   in place of the variables themselves. Thus, we obtain the expanded body
   `{20}-{6}`.

5. Since every pair of braces triggers the same algorithm for the number it
   contains, we go back to the step 1 with the number **20**. This time, our
   spell-table contains an entry for the number, so we get back _twenty_ and
   put it in the expanded body to obtain `twenty-{6}`. By performing similar
   steps for the second pair of braces we get the final spelling

        twenty-six

The second rule is pretty straightforward as well. Using only the first two
rules we can spell the first 1000 numbers: from 0 to 999.

The third rule has a consuming pattern and thus it becomes a _recursive rule_.
In a recursive rule the number of recursive invocations is remembered by the
algorithm. This allows for spelling number of huge magnitudes.

Let's take a look at the steps required to spell the number **1200001**.

1. Look the number up in the spell-table. No success.

2. Find a matching rule for the number. It is the third one, `(a)xxx = {a}
   {x}`.

3. Produce bindings for the pattern variables: `a = 1200`, `x = 1`.

4. Expand the body: `{1200, 1} {1}`. The comma in the first expansion has been
   put there for clarity. It represents the number of recursive invocations
   that the algorithm stores automatically.

5. Repeat the steps for each of the expansions. The second expansion is
   trivial. The matching rule for the first one is once again the recursive
   rule `(a)xxx = {a} {x}`.

6. The number **1200** will expand to `{1, 2} {200}` and, eventually, the whole
   body will become `{{1, 2} {2} hundred {0}, 1} {1}`.

The final step is to get the values from the lookup tables and put them into
the expanded body. Values for simple expansions are taken from the NUMBERS
table, whereas values for recursive expansions (those with a comma in our
notation) are taken from the ORDERS list.

In the English case, the NUMBERS table contains numbers 0—20, 30, 40, 50, 60,
70, 80, and 90.

The ORDERS list looks like this:

    ORDERS = ['', 'thousand', 'million', 'billion', ...]

As you might have already guessed, the number after the comma in the expansions
above can be used as an index into the ORDERS list. Below you can see how each
expansion is spelled out and how the spelling of the whole number is built up
from the components.

    {1, 2} {2} hundred {0}  -> one million two hundred
    {the above, 1}          -> one million two hundred thousand
    append {1} to the above -> one million two hundred thousand one

So, the final spelling for the number **1200001** is _one million two hundred
thousand one_.

---

Remember that using a variable multiple times in succession (like `x` in the
second and third rules) is just a syntactic sugar. The second rule could just
as well be written as

    abc = {a} hundred {bc}

Another thing worth mentioning is that `{0}` is only ever spelled when it is
standing all by itself. When it appears as a component of a larger number, it
is transformed into an empty string.

The steps outlined above are ***not*** the exact steps of the spelling
algorithm. The purpose of this document is to explain the rule syntax only. To
learn the actual steps performed by the algorithm, take a look at the
_SpellingAlgorithm.md_ file.
