# -*- coding: utf-8 -*-
import unittest
import numspell


LANGUAGES = ['en', 'es', 'ja', 'ru']


def build_setup(lang):
    def setup(self):
        self.speller = numspell.Speller(lang)
    return setup

def build_test(num, spelling):
    return lambda self: self.assertEqual(spelling, self.speller.spell(num))

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for lang in LANGUAGES:
        module = __import__("cases_" + lang)
        test_class = type(module.NAME,
                          (unittest.TestCase,),
                          { "setUp": build_setup(lang) })
        for num, spelling in module.TEST_CASES.items():
           setattr(test_class, "test_%s" % num, build_test(num, spelling))
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    unittest.main()
