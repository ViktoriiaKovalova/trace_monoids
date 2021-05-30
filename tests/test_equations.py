import string
import unittest
import typing as tp
import random

from trace_monoids.trace_monoid import TraceMonoid
from trace_monoids.equations import EquationSolver
from trace_monoids.words import Word, Alphabet, Letter


class SlowEquationSolver:
    def __init__(self, monoid: TraceMonoid):
        self.monoid = monoid

    def solve(self, u: Word, v: Word) -> tp.Optional[Word]:
        for letter in self.monoid.alphabet:
            for dependent in self.monoid.dependency[letter]:
                u_ = u.get_projection(letter, dependent)
                v_ = v.get_projection(letter, dependent)
                if len(u_) > len(v_):
                    return None
                if u_.word != v_.word[:len(u_)]:
                    return None
        return v.delete_lex_min_subsequence(u)

    def right_hand_solve(self, u: Word, v: Word) -> tp.Optional[Word]:
        res = self.solve(u.reversed(), v.reversed())
        return res.reversed() if res is not None else None


def generate_random_dependency(alphabet: Alphabet):
    graph: tp.Dict[Letter, tp.Set[Letter]] = {x: {x} for x in alphabet}
    for i in range(len(alphabet)):
        for j in range(i + 1, len(alphabet)):
            if random.randint(0, 1):
                graph[alphabet[i]].add(alphabet[j])
                graph[alphabet[j]].add(alphabet[i])
    return graph


def random_word(alphabet: Alphabet, length: int):
    return Word([alphabet[random.randint(0, len(alphabet) - 1)] for _ in range(length)])


class TestEquations(unittest.TestCase):
    def test_no_solution(self):
        monoid = TraceMonoid(alphabet={'a', 'b'}, dependency={'a': {'a', 'b'}, 'b': {'a', 'b'}})
        for solver in [EquationSolver(monoid), SlowEquationSolver(monoid)]:
            x = solver.solve(Word('ba'), Word('abb'))
            self.assertIsNone(x)

    def test_right_solve(self):
        monoid = TraceMonoid(alphabet={'a', 'b'}, dependency={'a': {'a', 'b'}, 'b': {'a', 'b'}})
        for solver in [EquationSolver(monoid), SlowEquationSolver(monoid)]:
            x = solver.right_hand_solve(Word('bb'), Word('abb'))
            self.assertEqual(x, Word('a'))

    def test_random(self):
        for num_letters in range(1, 5):
            for i in range(300):
                alphabet = string.ascii_letters[:num_letters]
                graph = generate_random_dependency(alphabet)
                monoid = TraceMonoid(alphabet=alphabet, dependency=graph)
                u, v = random_word(alphabet, random.randint(0, 5)), random_word(alphabet, random.randint(0, 5))
                solver, slow_solver = EquationSolver(monoid), SlowEquationSolver(monoid)
                self.assertEqual(solver.solve(u, v), slow_solver.solve(u, v))
                self.assertEqual(solver.right_hand_solve(u, v), solver.right_hand_solve(u, v))


if __name__ == '__main__':
    unittest.main()
