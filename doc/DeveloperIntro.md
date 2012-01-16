Introduction for Developers
===========================

This document describes the problem this project is trying to solve, its main
design decisions and its high-level architecture. Some implementation details
are also highlighted. Keep in mind, however, that the code itself is the best
documentation, much thought and effort have been put into it in order to make
it easy to understand, extend and contribute to.


## Background ##

Every human language has slightly varying rules for spelling numerals as well
as a number of exceptions specific to each language.

Take, for instance, the number **1300000**. In English it is spelled

    one million one hundred thousand

In Spanish it would be

    un millón cien mil

Here we can already see one trait of Spanish which is not present in English.
_Uno_ becomes _un_ when followed by a masculine noun like _millón_, _billón_,
etc. In a somewhat similar fashion, _ciento_ becomes _cien_ when followed by a
noun, this time the gender doesn't matter. We need to take these peculiarities
into account when designing a spelling algorithm.

If we continue counting up to two million, we'll see another interesting trait
of Spanish language. _Two million_ is spelled _dos millones_ because Spanish
millions, billions, etc. change their grammatical number, unlike English ones.
In Russian they have even more variations:

    1 million → 1 миллион
    2 million → 2 миллиона
    5 million → 5 миллионов

So, what is the best way to design an algorithm that could be flexible enough
to accommodate numerous variations of different human languages yet be simple
enough for a programmer to understand it and extend it without much effort?

The answer to the question above is reflected in the two basic principles that
form the foundation of this project:

1. The project is highly modularized allowing a programmer to chain multiple
   modules together in order to get the desired processing sequence.

2. For each human language there is a set of rules (rather than a separate
   algorithm) defining the way any given number should be spelled out in that
   language.

So, broadly speaking, there is a single algorithm used to generate spelling for
every supported human language. There may be one or two extensions to the
algorithm for some of the languages, but the core of each language is defined
by a set of rules written using a simple syntax. The algorithm processes
numbers by applying those rules and dealing with all the irregularities that
any particular human language has.

The steps comprising the whole spelling algorithm are described in the
_SpellingAlgorithm.md_ file. The syntax used to define the rules of number
decomposition is explained in the _RuleSyntax.md_ file.


## Dealing With Irregularities and Exceptions ##

In order to deal with dissimilar irregularities between different languages,
the concept of **passes** has been introduced. Applying the rules to decompose
a number into logical components substitutes for the first pass of the whole
spelling process. For some languages it may be the only one required, English
is the case. For most languages, however, a number of additional processing
routines is needed in order to obtain the final spelling.

Let's first look at how we can fix the spelling of **1,000,000** in Spanish. In
fact, there's a couple of irregularities involving the numeral **1**:

    1,000,000   → un millón
    21,000,000  → veintiún millones

In each of these examples any order higher than **1,000** can be used instead
of **millón**, they all change in the same manner. Let's focus on the **un**
part first, we'll deal with the plural form later.

After decomposing the number **1,000,000** into components, we'll get a list
`['1', 1]` where '1' can be replaced with one lookup and **1** denotes the
index into the `ORDERS` list which would yield the word _millón_. Once we have
this list, we can analyze it. If we had a rule saying

    if you encounter the numeral '1' and an order immediately following it,
    spell '1' as _un_

it would solver the problem!

In a similar fashion, if we had a rule saying

    if you encounter an order preceded by a numeral greater than '1', spell it
    in plural form

we would get the correct spelling for huge numbers like millions, billions,
etc.

The **listparse** submodule allows you to define such rules using a template
string that will act upon a list and transform its elements according to those
rules. See the submodule's docstring and the _TemplateSyntax.md_ file for the
detailed information on the subject.
