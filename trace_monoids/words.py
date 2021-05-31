from __future__ import annotations
import typing as tp
from collections import defaultdict

Letter = str
Alphabet = tp.Sequence[Letter]


class Word:
    def __init__(self, word: tp.Sequence[Letter]):
        self.word = word

    def __len__(self):
        return len(self.word)

    def __getitem__(self, index: int):
        return self.word[index]

    def __eq__(self, another_word: Word):
        return list(self.word) == list(another_word.word)

    def __str__(self):
        return str(self.word)

    def __repr__(self):
        return str(self.word)

    def reversed(self) -> Word:
        """
        :return: reversed word
        """
        return Word(list(reversed(self.word)))

    def create_indices_mapping(self, other: Word) -> tp.Dict[int, int]:
        """
        Creates mapping of indices from self to corresponding letters of other word
        """
        u, v = self.word, other.word
        ind: tp.Dict[int, int] = {}
        cnt = defaultdict(int)
        pos: tp.Dict[tp.Tuple[Letter, int], int] = {}

        for i, letter in enumerate(u):
            cnt[letter] += 1
            pos[(letter, cnt[letter])] = i

        cnt = defaultdict(int)
        for i, letter in enumerate(v):
            cnt[letter] += 1
            if (letter, cnt[letter]) in pos:
                ind[pos[(letter, cnt[letter])]] = i

        return ind

    def get_projection(self, a: Letter, b: Letter):
        """
        Calculates pi_{a, b}(word)
        """
        return Word([letter for letter in self.word if letter == a or letter == b])

    def calculate_prefix_counter(self, alphabet: Alphabet) -> tp.List[tp.Dict[Letter, int]]:
        """
        Calculates structure containing information about number of each letter for each prefix.
        :param: alphabet - alphabet
        :return: List of dicts. result[i][l], contains number of letters l in prefix of len i.
        """
        u = self.word
        prefix_counter = [{letter: 0 for letter in alphabet} for i in range(len(u) + 1)]
        for prefix_len in range(1, len(u) + 1):
            for letter in alphabet:
                prefix_counter[prefix_len][letter] = prefix_counter[prefix_len - 1][letter] + int(letter == u[prefix_len - 1])
        return prefix_counter

    def delete_lex_min_subsequence(self, v: Word) -> Word:
        """
        Deletes lexicographically minimal subsequence that contains the same letter as v from self
        :return: self without this subsequence
        """
        result = []
        to_delete = defaultdict(int)
        for letter in v:
            to_delete[letter] += 1

        for letter in self.word:
            if to_delete[letter]:
                to_delete[letter] -= 1
            else:
                result.append(letter)
        return Word(result)
