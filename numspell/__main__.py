import argparse
import os         # listdir, path.dirname
import re         # compile
import sys        # argv

import numspell

from argparse_formatter import FlexiFormatter


def discover_available_languages():
    lang_re = re.compile(r'^spelling_([a-z]{2}).py$')
    f = lambda x: lang_re.match(x)
    filenames = os.listdir(os.path.dirname(sys.argv[0]))
    return [x.group(1) for x in map(f, filenames) if x]

def main():
    DEBUG_DESCR = """
Print all of the steps taken to produce the spelling for a given number. \
Useful for debugging purposes and to get to know the algorithm behind \
the process."""

    LANG_DESCR = """
Language code in ISO 639-1 format. Default: en.

Specify the language to spell with or to use when checking the user-provided \
spelling (see the --check option below).

Currently supported languages:
  """ + '\n  '.join(discover_available_languages())

    CHECK_DESCR = """
Provide your own spelling for numspell to check and correct.

If the spelling is correct, exit with 0 status code. If the spelling is \
wrong, output the correct spelling to stdout and exit with a non-zero \
status code."""

    parser = argparse.ArgumentParser(prog="spellnum",
                description='Spell integers in various languages',
                formatter_class=FlexiFormatter)
    parser.add_argument('num', metavar='number', type=int,
            help="an integer to spell")
    parser.add_argument('-d', '--debug', action='store_const',
            const=True, default=False, help=DEBUG_DESCR)
    parser.add_argument('-l', '--lang', type=str, default='en',
            help=LANG_DESCR)
    parser.add_argument('-c', '--check', metavar='<spelling>', type=str,
            help=CHECK_DESCR)
    args = parser.parse_args()

    speller = numspell.Speller(args.lang, args.debug)
    if args.check:
        result = speller.check(args.num, args.check)
        if result:
            print result
            exit(1)
    else:
        print speller.spell(args.num)


if __name__ == '__main__':
    main()
