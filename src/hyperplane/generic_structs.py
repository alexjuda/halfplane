import typing as t
import collections.abc

import more_itertools as mitt


class FrozenOrderedSet(collections.abc.Set, collections.abc.Hashable):
    """
    Immutable, set-like container that retains the order of elements. Hashable.
    """

    def __init__(self, iterable: t.Iterable):
        ordered = list(mitt.unique_everseen(iterable))

        self._set = frozenset(ordered)
        self._list = ordered

    # -------- Set --------
    def __contains__(self, x):
        return x in self._set

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._set)

    # -------- Hashable --------
    def __hash__(self):
        return hash(self._set)
