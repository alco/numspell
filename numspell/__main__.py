import numspell

def main():
    import argparse

    parser = argparse.ArgumentParser(prog="spellnum", description='Spell integers in various languages')
    parser.add_argument('num', metavar='number', type=int, help="an integer to spell")
    parser.add_argument('--lang', '-l', type=str, default='en', help="language code in ISO 639-1 format")
    args = parser.parse_args()

    speller = numspell.Speller(args.lang)
    print speller.spell(args.num)

if __name__ == '__main__':
    main()
