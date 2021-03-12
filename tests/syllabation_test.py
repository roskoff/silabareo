import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from utils.hyphenate import Hyphenator

class TestSyllabation(unittest.TestCase):
    def setUp(self):
        with open('build/patterns_for_hyphen.txt', mode='r', encoding='UTF-8') as patternfile:
            self.patterns = (patternfile.read().replace('UTF-8\nLEFTHYPHENMIN 1\nRIGHTHYPHENMIN 1\n', '').replace('\n', ' '))
        self.exceptions = ""

        hyphenator = Hyphenator(self.patterns, self.exceptions)
        self.hyphenate_word = hyphenator.hyphenate_word

        return super().setUp()

    def test_regla01(self):
        with open("tests/regla_01.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_01_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla02(self):
        with open("tests/regla_02.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_02_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla03(self):
        with open("tests/regla_03.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_03_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla04(self):
        with open("tests/regla_04.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_04_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla05(self):
        with open("tests/regla_05.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_05_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla06(self):
        with open("tests/regla_06.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_06_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla07(self):
        with open("tests/regla_07.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_07_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla08(self):
        with open("tests/regla_08.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_08_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla09(self):
        with open("tests/regla_09.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_09_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla10(self):
        with open("tests/regla_10.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_10_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla11(self):
        with open("tests/regla_11.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_11_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla12(self):
        with open("tests/regla_12.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_12_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla13(self):
        with open("tests/regla_13.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_13_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_regla14(self):
        with open("tests/regla_14.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/regla_14_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def test_reglas15_al_18(self):
        with open("tests/reglas_15_16_17_18.txt", "r") as f:
            words = f.read().splitlines()
        with open("tests/reglas_15_16_17_18_expected.txt", "r") as f:
            expected_values = f.read().splitlines()

        self.assertEqual(len(words), len(expected_values))

        for word, expected_value in zip(words, expected_values):
            self.assertEqual('-'.join(self.hyphenate_word(word)), expected_value)

    def tearDown(self):
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()