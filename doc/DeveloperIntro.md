Introduction for Developers
===========================

This document describes design goals of this project as well as the problems
it is trying to solve. Some implementation details are also highlighted. Keep
in mind, however, that the code itself is the best documentation, much thought
and effort have been put into it in order to make it easy to understand,
extend and contribute to.


## Background ##

Every human language has slightly varying rules for spelling numerals as well
as a number of exceptions specific to each language.

Take, for instance, the number `1300000`. In English it is spelled

    one million one hundred thousand

In Spanish it would be

    un millón cien mil

Here we can already see one trait of Spanish which is not present in English.
**Uno** becomes **un** when followed by a masculine noun like **millón**,
**billón**, etc. So we need to take this peculiarity into account when
designing a spelling algorithm.

In a somewhat similar fashion, **ciento** becomes **cien** when followed by a
noun, this time the gender doesn't matter.

If we continue counting up to two million, we'll see another interesting trait
of Spanish language. **Two million** is spelled **dos millones** in Spanish.
So, Spanish millions, billions, etc. change their grammatical number, unlike
English ones. In Russian they have even more variations:

    1 million → 1 миллион
    2 million → 2 миллиона
    5 million → 5 миллионов

So, what is the best way to design an algorithm that could be flexible enough
to acommodate numerous variations of different human languages yet be simple
enough for a programmer to understand it and extend it without much effort?

The answer to the question above is reflected in the two basic principles that
form the foundation of this project:

1. The project is highly modularized allowing a programmer to chain multiple
   modules together in order to get the desired processing sequence.

2. For each human language there is a set of rules (rather than a separate
   algorithm) defining the way any given number should be spelled out in that
   language.

So, broadly speaking, there is a single algorithm used to generate spelling
for every supported human language. There may be one or two extensions to the
algorithm for some of the languages, but the core of each language is defined
by a set of rules written using a simple syntax. The algorithm processes
numbers by applying those rules and dealing with all the irregularities that
any particular human lanuage has.


## Dealing With Irregularities and Exceptions ##

In order to deal with dissimilar irregularities between different languages,
the concept of _passes_ has been introduced. The algorithm described in the
previous section substitutes for the first pass of the whole spelling process.
For some languages it may be the only one required, English is the case. For
most languages, however, a number of additional processing routines is needed
in order to obtain the final spelling.

Let's first look at how we can fix the spelling of `1,000,000` in Spanish. In
fact, there are three irregularities, each of which involves the numeral `1`:

    1,000,000   → un millón
    21,000,000  → veintiún millones
    101,000,000 → cientoún millones

In each of this examples any order higher than `1,000` can be used instead of
`millón`, they all change in the same manner. Let's focus on the `un` part
first, we'll deal with the plural form later.
