import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from utils.hyphenate import Hyphenator
from syllabation_adjustment import SyllableAdjustment

class TestSyllabationAdjustment(unittest.TestCase):
    def setUp(self):
        with open('build/patterns_for_hyphen.txt', mode='r', encoding='UTF-8') as patternfile:
            self.patterns = (patternfile.read().replace('UTF-8\nLEFTHYPHENMIN 1\nRIGHTHYPHENMIN 1\n', '').replace('\n', ' '))
        self.exceptions = ""

        hyphenator = Hyphenator(self.patterns, self.exceptions)
        self.hyphenate_word_as_string = hyphenator.hyphenate_word_as_string
        syllable_adjustment = SyllableAdjustment()
        self.addjust_syllables = syllable_adjustment.adjust

        return super().setUp()

    def test_general(self):
        with open("tests/words_that_need_adjustment.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/words_with_syllables_adjusted.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            hyphenated_word = self.hyphenate_word_as_string(word)
            self.assertEqual(self.addjust_syllables(hyphenated_word), expected_value)

    def tearDown(self):
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()