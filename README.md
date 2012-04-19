numspell
========

A Python module for spelling numbers.

Here's a quick demo of what it can do.

```sh
$ ./spellnum 321
three hundred twenty-one

$ ./spellnum 10500090
ten million five hundred thousand ninety

$ ./spellnum -les 3002
tres mil dos

$ ./spellnum -lru 90532701000
девяносто миллиардов пятьсот тридцать два миллиона семьсот одна тысяча

$ ./spellnum -lja 34101
三万四千百一    # hiragana spelling coming later
```

From the user's point of view, **numspell** is a Python module with a single
public class — the `Speller`. A convenience command-line tool called
**spellnum** is included in the distribution.


## Command-Line Interface ##

Let the utility itself describe how it is supposed to be used.

```shell
$ spellnum -h
usage: spellnum [-hd] [--lang=LANG] [--check=<spelling>] <number>

Spell a number using one of the available languages or check a user-provided
spelling for correctness.

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

  -l LANG, --lang=LANG
      Language code in ISO 639-1 format. Default: en.

      Specify the language to spell with or to use when checking the user-
      provided spelling (see the --check option below).

      Currently supported languages:
        en (English)
        es (Spanish)
        ja (Japanese)
        ru (Russian)

  -c <spelling>, --check=<spelling>
      Provide your own spelling for numspell to check and correct.

      If the spelling is correct, exit with 0 status code. If the spelling is
      wrong, output the correct spelling to stdout and exit with a non-zero
      status code.
```


## Module API ##

The API of the **numspell** module is very straightforward. It can be
explained in two words: `spell` and `check`.

```python
import numspell

# The language code is passed to the Speller class constructor.
gentleman = numspell.Speller('en')

# Pass an integer to the 'spell' method
# and it will return a string with its spelling.
assert(gentleman.spell(1300) == 'one thousand three hundred')
assert(gentleman.spell(10700010) == 'ten million seven hundred thousand ten')

# Here we use the 'es' language code to spell some numbers in Spanish.
torero = numspell.Speller('es')
assert(torero.spell(1989) == 'mil novecientos ochenta y nueve')

# numspell can also check and correct your spelling.
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

If you're looking for a more detailed description of the **numspell** module
API, take a look at its help:

    $ python
    >>> import numspell
    >>> help(numspell)

If, however, you would like to dive deeper and find out how you can add a new
spelling language, port the spelling algorithm to another programming language
or contribute to the project in some other way, take a look at developer
documentation in the _doc_ directory or view the online [wiki][1].


## Contributing ##

The project will have a roadmap at some point in the future. For now, some of
the tasks are outlined in the _TODO_ file.

The _doc_ directory contains developer documentation which describes the design
and implementation of the modules that **numspell** is comprised of. The
documentation is also viewable online on the project's [wiki][1]. Here's a
brief overview of the documentation files:

* _Developer-Introduction.md_ describes the goals, design decisions and
  high-level architecture of the project.

* _Spelling-Algorithm.md_ outlines the steps of the spelling algorithm and
  explains how each step is implemented.

* _Rule-Syntax.md_ explains the syntax for defining rules by which a number is
  decomposed into logical elements.

* _Template-Syntax.md_ explains the template string syntax used by the
  **listparse** submodule. It allows to transform the logical elements of a
  number to adjust for possible exceptions and irregularities of a particular
  human language.


## Contact Info ##

Your comments and questions are most welcome. My name is Alex and I can be
reached at alcosholik@gmail.com. You may also follow me on
[GitHub](https://github.com/alco) and
[Twitter](https://twitter.com/true_droid).


## License ##

**numspell** is Copyright (c) 2012 Alexei Sholik. It is distributed under the
terms of the MIT license. See the LICENSE file for the full license text.


  [1]: https://github.com/alco/numspell/wiki
