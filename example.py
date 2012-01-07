# -*- coding: utf-8 -*-
import numspell

gentleman = numspell.Speller('en')
assert(gentleman.spell(1300) == 'one thousand three hundred')
assert(gentleman.spell(10700010) == 'ten million seven hundred thousand ten')

torero = numspell.Speller('es')
assert(torero.spell(1989) == 'mil novecientos ochenta y nueve')
assert(torero.check(10007, 'diez mil siete') is None)
assert(torero.check(1, 'dos') == 'uno')
