from trace_monoids.trace_monoid import TraceMonoid
from trace_monoids.words import Word, Letter
import typing as tp


class EquationSolver:
    """
    This class solve equations of form [u][x]=[v], and [x][u]=[v] in trace monoids
    """
    def __init__(self, monoid: TraceMonoid):
        self.monoid = monoid

    def solve(self, u: Word, v: Word) -> tp.Optional[Word]:
        """
        Solves equation [u][x] = [v] and returns word from class [x] if solution exists.
        Otherwise, returns None.
        """
        # build indices mapping and check that all indices of u have corresponding index in v
        ind: tp.Dict[int, int] = u.create_indices_mapping(v)
        if len(ind) != len(u):
            return None

        pref_u: tp.List[tp.Dict[Letter, int]] = u.calculate_prefix_counter(self.monoid.alphabet)
        pref_v: tp.List[tp.Dict[Letter, int]] = v.calculate_prefix_counter(self.monoid.alphabet)

        for i, letter in enumerate(u.word):
            j = ind[i]
            for second_letter in self.monoid.dependency[letter]:
                if pref_u[i][second_letter] != pref_v[j][second_letter]:
                    return None

        return v.delete_lex_min_subsequence(u)

    def right_hand_solve(self, u: Word, v: Word) -> tp.Optional[Word]:
        """
        Solves equation [x][u] = [v] and returns word from class [x] if solution exists.
        Otherwise, returns None.
        """
        result = self.solve(u.reversed(), v.reversed())
        if result is None:
            return None
        return result.reversed()
