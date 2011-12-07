DISCLAIMER
==========

_This document is written by applying the concept of 'wishful thinking'. In
other words, it describes the desired functionality which is **NOT** implemented
yet._

_If you find it confusing, take a look at this short and very nicely written
introduction to_ [Readme Driven Development][1] _by_ Tom Preston-Werner, _its
author and evangelist._

_As soon as the contents of this README reflects the actual functionality that
is available to the end user, this disclaimer will disappear._

  [1]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html

spellnum
========

A Python module for spelling numbers.

## User Dimension

From the user's point of view, **spellnum** can be used either as a command-line
utility or as a module by `import`ing it in your own Python code.

### Command-Line Interface

Let the utility itself describe how it is supposed to be used.

```shell
$ python spellnum.py -h
usage: spellnum.py [-hd] [--lang=LANG] [--check=<spelling>] <number>

Spell a number in one of the available languages
or check a user's spelling for correctness.


Positional arguments:

  number
      An integer to spell. It has to be a simple number without spaces or
      punctuation marks to separate thousands.

Optional arguments:

  -h, --help
      Show this help message and exit.

  -d, --debug
      Print all of the steps taken to produce the spelling for a given number.
      Useful for debugging purposes and to get to know the algorithm behind
      the process.

  --lang=LANG
      Language code in ISO 639-1 format. Default: en.

      Specify the language to spell with or to use when checking the user-
      provided spelling (see the --check option below).

      Currently supported languages:
        de (German)
        en (English)
        es (Spanish)
        fr (French)
        it (Italian)
        ja (Japanese)
        ru (Russian)
        uk (Ukrainian)

  --check=<spelling>
      Provide your own spelling for spellnum to check and correct.

      If the spelling is correct, exit with 0 status code. If the spelling is
      wrong, output the correct spelling to stdout and exit with a non-zero
      status code.
```


### Module API

The API for the Python module **spellnum** is very straightforward. It can be
explained with this simple example:

```python
import spellnum

# The language code is passed to the Speller class constructor.
gentleman = spellnum.Speller('en')

# Pass an integer to the 'spell' method
# and it will return a string with its spelling.
assert(gentleman.spell(1300) == 'one thousand three hundred')
assert(gentleman.spell(10700010) == 'ten million seven hundred thousand ten')

# Here we use the 'es' language code to spell some numbers in Spanish.
torero = spellnum.Speller('es')
assert(torero.spell(1989) == 'mil novecientos ochenta y nueve')

# spellnum can also check and correct your spelling.
#
# The 'check' method returns a string with correct spelling if the spelling
# provided by the user is wrong.
#
# It returns None otherwise.
assert(torero.check(10007, 'diez mil siete') is None)
assert(torero.check(1, 'dos') == 'uno')
```

This example is taken from the _example.py_ script in the root directory of the
project. You can actually run it yourself to make sure that all of the
assertions hold true.

If you're looking for a more detailed description of the **spellnum** module
API, take a look at its help:

    $ python
    >>> import spellnum
    >>> help(spellnum)

If, however, you would like to dive deeper and find out how you can add a new
spelling language, port the spelling algorithm to another programming language
or contribute to the project in some other way, please read on.

## Developer Dimension

This section describes design goals of this project as well as the problems it
is trying to solve. Some implementation details are also highlighted. Keep in
mind, however, that the code itself is the best documentation, much thought and
effort have been put in it in order to make it easy to understand, extend and
contribute to.

### Background

Every human language has slightly varying rules for spelling numerals as well
as a number of exceptions specific to each language.

Take, for instance, the number `1300000`. In English it is spelled

    one million one hundred thousand

In Spanish it would be

    un millón cien mil

Here we can already see one trait of Spanish which is not present in
English. **Uno** becomes **un** when followed by a masculine noun like
**millón**, **billón**, etc. So we need to take this peculiarity into account
when designing a spelling algorithm.

In a somewhat similar fashion, **ciento** becomes **cien** when followed by a
noun, this time the gender doesn't matter.

If we continue counting up to two million, we'll see another interesting trait
of Spanish language. **Two million** is spelled **dos millones** in Spanish. So,
Spanish millions, billions, etc. change their grammatical number, unlike English
ones. In Russian they have even more variations:

    1 million → 1 миллион
    2 million → 2 миллиона
    5 million → 5 миллионов

So, what is the best way to design an algorithm that could be flexible enough to
acommodate numerous variations of different human languages yet be simple enough
for a programmer to understand it and extend it without much effort?

The answer to the question above is reflected in the two basic principles that
form the foundation of this project:

1. The project is highly modularized allowing a programmer to chain multiple
modules together in order to get the desired processing sequence.

2. For each human language there is a set of rules (rather than a separate
algorithm) defining the way any given number should be spelled out in that
language.

So, broadly speaking, there is a single algorithm used to generate spelling for
every supported human language. There may be one or two extensions to the
algorithm for some of the languages, but the core of each language is defined by
a set of rules written using a simple syntax. The algorithm processes numbers by
applying those rules and dealing with all the irregularities that any particular
human lanuage has.

### The Rule Syntax

The rule syntax is based on pattern matching. Every rule has two parts: the _pattern_ and the _body_, separated by an equals sign (=). The pattern is matched against the given number to determine whether the rule is applicable or not in terms of the given number.

Since the best way to learn is to learn by example, let's take a look at the rule set for the English language.

    ab = {a0}-{b}
    axx = {a} hundred {x}
    (a)xxx = {a} {x}

That's all we need to define an English speller! Well, almost all. Of course, we will also need a lookup table for the numbers like one, ten, twenty, etc. But more on this later.

Let's look at the first rule -- `ab = {a0}-{b}`. The part to the left of the equals sign--the pattern--has two variables: `a` and `b`. A variable is any of the 26 English letters, each variable can match one and only one digit. So, the pattern `ab` will match any two-digit number, like 11, 26, 94, and so on.

Now, the pattern of a rule has matched the given number, we take that rule and expand its body. In other words, we determine what values will the variable from the pattern will get and then we substitute those values in place of variable in the body of the rule--the part of the rule to the right of the equals sign.

Moving on to the rule's body. Every sequence of English letters or digits enclosed within braces (`{` and `}`) is called an _expansion_. It basically means "take the contents within a pair of braces and pass it through the same algorithm", i.e. spell the number inside those braces.

It's time to describe the spelling algorithm. Let's take the number 26.

1. First, we will look the number up in the lookup table. In the case with the English language, it's not there.

2. Next, we will try to match the rules defined for English against the number. The rules are matched in order the are written, one at a time. In our case, the matching rule is `ab = {a0}-{b]`.

3. After the matching process we have two variables, `a` and `b`, which have the values `2` and `6`, respectively.

4. We will then expand the body of the matching rule substituting variable values in place of the variables themselves. Thus, we obtain the expanded body `{20}-{6}`.

5. Since every pair of braces triggers this same algorithm for the number it contains, we will go back to the step 1 with the number `20`. This time, our lookup table contains an entry for the number, so we get back `twenty` and put it in the expanded body to obtain `twenty-{6}`. By performing similar steps for the second pair of braces we will finally get the spelling, which is

        twenty-six

The only new syntax in the second rule is using the variable `x` twice. This is just a syntactic sugar. The second rule could just as well be written as

    abc = {a} hundred {bc}

So, repeating the variable name in the pattern multiple times is a way to say to the rule parser "I'd like to store these _N_ consecutive digits in the variable `x` so that I don't need to come up with many variable names and so that I could save me some typing when writing the body of the rule".

The third rule is tricky. It is a so called _cycling rule_ because it contains parentheses. It works differently from the ones we have looked at before.

...

### The Spelling Algorithm

1. First, look the number up in the lookup table. If it's there, get the spelling from the table and go to **Step 6**. If it's not, proceed to the next step.

2. Match the rules in order, one at a time, against the given number. Specifically, match the pattern of each consecutive rule until it is matched. If no rule has matched, raise an exception. Otherwise, take the matching rule and proceed to the next step.

3. Extract the values of the variables defined in the matching rule's pattern from the given number. This step will produce a mapping from variables to digits which will be used in the next step.

4. Expand the body of the matching rule by substituting variable values in place of the variable names. This step produces an expanded body with no variables left in it.

5. For every pair of braces in the matching rule's body, run this algorithm recursively, passing as an argument the number enclosed between the braces.

6. Squash all serieses of the consecutive orders (if there are any) by leaving only the leftmost order and dropping the rest in each one of such serieses.


### Dealing With Irregularities and Exceptions

In order to deal with dissimilar irregularities between different languages, the concept of _passes_ has been introduced. The algorithm described in the previous section substitutes for the first pass of the whole spelling process. For some languages it may be the only one required, English is the case. For most languages, however, a number of additional processing routines is needed in order to obtain the final spelling.

Let's first look at how we can fix the spelling of `1,000,000` in Spanish. In fact, there are three irregularities, each of which involves the numeral `1`:

    1,000,000   → un millón
    21,000,000  → veintiún millones
    101,000,000 → cientoún millones

In each of this examples any order higher than `1,000` can be used instead of `millón`, they all change in the same manner. Let's focus on the `un` part first, we'll deal with the plural form later.
