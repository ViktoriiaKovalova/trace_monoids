import string
import unittest
import random

from trace_monoids.words import Word


class TestEquality(unittest.TestCase):
    def test_different_types(self):
        self.assertEqual(Word(['a', 'b', 'c']), Word('abc'))


class TestFindProjection(unittest.TestCase):
    def test_empty_word(self):
        word = Word("")
        projection = word.get_projection('a', 'b').word
        self.assertEqual(len(projection), 0)

    def test_same_word(self):
        word = Word("abbaa")
        projection = word.get_projection('a', 'b')
        self.assertEqual(list(word.word), list(projection.word))

    def test_many_letters(self):
        word = Word(string.ascii_lowercase)
        for i in range(100):
            str_sz = len(word.word)
            fir = random.randint(0, str_sz - 1)
            sec = random.randint(0, str_sz - 1)
            expected = word.word[fir] + word.word[sec]
            if fir > sec:
                expected = word.word[sec] + word.word[fir]
            elif fir == sec:
                expected = word.word[fir]
            projection = word.get_projection(word.word[fir], word.word[sec])
            self.assertEqual(list(projection.word), list(expected))
            word.word = ''.join(random.sample(word.word, len(word.word)))


class TestIndicesMapping(unittest.TestCase):
    def test_empty(self):
        word = Word('')
        word2 = Word('')
        self.assertEqual(word.create_indices_mapping(word2), {})

    def test_extra_letter(self):
        word = Word('aab')
        word2 = Word('aaba')
        self.assertEqual(word.create_indices_mapping(word2), {i: i for i in range(3)})

    def test_no_mapping(self):
        word = Word('aa')
        word2 = Word('bba')
        self.assertEqual(word.create_indices_mapping(word2), {0: 2})

    def test_big(self):
        for i in range(100):
            word = random.sample(string.ascii_lowercase, 5)
            word2 = random.sample(string.ascii_lowercase, 10)
            indices = Word(word).create_indices_mapping(Word(word2))
            for x, y in indices.items():
                self.assertEqual(word[x], word2[y])
            self.assertEqual(len(set(word).intersection(set(word2))), len(indices))


class TestPrefixCounter(unittest.TestCase):
    def test_simple(self):
        word = Word('abbb')
        result = word.calculate_prefix_counter(['a', 'b'])
        self.assertEqual(result[0]['a'], 0)
        self.assertEqual(result[0]['b'], 0)
        self.assertEqual(result[1]['b'], 0)
        self.assertEqual(result[1]['a'], 1)
        self.assertEqual(result[4]['b'], 3)
        self.assertEqual(result[4]['a'], 1)

    def test_random(self):
        for i in range(100):
            max_letter = len(string.ascii_lowercase) - 1
            letters = string.ascii_lowercase
            word = [letters[random.randint(0, max_letter)] for _ in range(10)]
            indices = Word(word).calculate_prefix_counter(letters)
            for letter in letters:
                for pref in range(11):
                    if not pref:
                        self.assertEqual(indices[pref][letter], 0)
                    elif word[pref - 1] == letter:
                        self.assertEqual(indices[pref][letter], indices[pref - 1][letter] + 1)
                    else:
                        self.assertEqual(indices[pref][letter], indices[pref - 1][letter])


class TestDeleteSubsequence(unittest.TestCase):
    def test_delete_empty(self):
        word = Word("abc")
        self.assertEqual(word.delete_lex_min_subsequence(Word('')), word)

    def test_delete_all(self):
        word = Word('abb')
        self.assertEqual(word.delete_lex_min_subsequence(word), Word(''))

    def test_multiple_letters(self):
        word = Word("abcabbb")
        self.assertEqual(word.delete_lex_min_subsequence(Word("abb")), Word('cabb'))


class TestReversed(unittest.TestCase):
    def test_empty(self):
        word = Word("")
        self.assertEqual(word, word.reversed())

    def test_reverse(self):
        word = Word("abca")
        self.assertEqual(word.reversed(), Word("acba"))


if __name__ == '__main__':
    unittest.main()
