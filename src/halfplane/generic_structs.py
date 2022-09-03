import typing as t
import collections.abc

import more_itertools as mitt

T = t.TypeVar("T")


class FOSet(
    collections.abc.Set[T],
    collections.abc.Hashable,
    collections.abc.Collection[T],
):
    """
    Frozen Ordered Set. Immutable, set-like container that retains the order of
    elements. Hashable.
    """

    def __init__(self, iterable: t.Iterable[T]):
        ordered = list(mitt.unique_everseen(iterable))

        self._set = frozenset(ordered)
        self._list = ordered

    # -------- Set --------
    def __contains__(self, x: T):
        return x in self._set

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._set)

    # -------- Hashable --------
    def __hash__(self):
        return hash(self._set)

    # -------- Collection --------
    def __reversed__(self):
        return FOSet(reversed(self._list))

    def __getitem__(self, index):
        return self._list[index]

    # -------- Object --------
    def __repr__(self):
        return f"{type(self).__name__}({self._list})"
