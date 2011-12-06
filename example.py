# -*- coding: utf-8 -*-
import spellnum

# The language is passed to the Speller class constructor.
gentleman = spellnum.Speller('en')

# Pass an integer to the 'spell' method
# and it will return a string with the spelling.
assert(gentleman.spell(1300) == 'one thousand three hundred')
assert(gentleman.spell(10700010) == 'ten million seven hundred thousand ten')

# Here we use the 'es' language code to spell some numbers in Spanish
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
