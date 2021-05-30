import networkx as nx
import matplotlib.pyplot as plt
import typing as tp
from trace_monoids.words import Letter, Word, Alphabet


class TraceMonoid:
    """
    Class represents information about trace monoid, defined by its alphabet and dependency relation.
    """
    def __init__(self, alphabet: Alphabet, dependency: tp.Dict[Letter, tp.Set[Letter]]):
        self.alphabet = alphabet
        self.dependency = dependency
        for letter in self.alphabet:
            if letter not in dependency or letter not in dependency[letter]:
                raise ValueError("Letter should be in dependency relation with itself")
        for letter, dep_letters in dependency.items():
            for second_letter in dep_letters:
                if letter not in dependency[second_letter]:
                    raise ValueError("The dependency relation should be symmetric")

    def words_are_equivalent(self, u: Word, v: Word):
        """
        Checks whether two words are equivalent in this trace monoid
        """
        for letter, dependent_letters in self.dependency.items():
            for second_leter in dependent_letters:
                if u.get_projection(letter, second_leter) != v.get_projection(letter, second_leter):
                    return False
        return True

    def visualize_dependency(self):
        """
        Draws picture of dependency graph.
        """
        g = nx.Graph()
        g.add_nodes_from(self.alphabet)
        g.add_edges_from({(key, val) for key, values in self.dependency.items() for val in values})
        nx.draw_networkx(g, node_size=300, node_color="#D0F9FD", pos=nx.spring_layout(g))
        plt.show()
