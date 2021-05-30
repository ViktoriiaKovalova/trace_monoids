import unittest
from trace_monoids.trace_monoid import TraceMonoid
from trace_monoids.words import Word


class TestTraceMonoid(unittest.TestCase):
    def test_incorrect_monoid(self):
        graph = {'a': {'b'}, 'b': {'b'}}
        self.assertRaises(ValueError, TraceMonoid, alphabet=graph.keys(), dependency=graph)

    def test_simple(self):
        graph = {'a': 'a'}
        monoid = TraceMonoid(alphabet=graph.keys(), dependency=graph)
        self.assertEqual(monoid.words_are_equivalent(Word('a'), Word('a')), True)

    def test_not_equivalent(self):
        graph = {'a': ['a', 'b'], 'b': ['b', 'a']}
        monoid = TraceMonoid(alphabet=graph.keys(), dependency=graph)
        self.assertEqual(monoid.words_are_equivalent(Word('abba'), Word('abab')), False)


if __name__ == '__main__':
    unittest.main()
