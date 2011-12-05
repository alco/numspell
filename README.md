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
      show this help message and exit.

  -d, --debug
      Print all of the steps taken to produce the spelling for a given number.
      Useful for debugging purposes and to get to know the algorithm behind
      the process.

  -l LANG, --lang=LANG
      Language code in ISO 639-1 format.

      Specify the language to spell with or to use when checking the user-
      provided spelling (see the --check option below).

      Default: en.

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


### Modulde API

## Developer Dimension
