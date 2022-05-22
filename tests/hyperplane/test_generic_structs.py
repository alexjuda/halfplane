from hyperplane import generic_structs
import hypothesis as h
import hypothesis.strategies as st


def _hashables():
    return st.integers()


class TestFrozenOrderedSet:
    @h.given(items=st.lists(_hashables()))
    def test_equal_to_plain_set(self, items):
        plain_set = set(items)

        o_set = generic_structs.FrozenOrderedSet(items)
        assert o_set == plain_set

    @h.given(items=st.lists(_hashables(), unique=True))
    def test_retains_order(self, items):
        o_set = generic_structs.FrozenOrderedSet(items)
        assert list(o_set) == items

    @h.given(
        set1=st.builds(generic_structs.FOSet, st.iterables(_hashables())),
        set2=st.builds(generic_structs.FOSet, st.iterables(_hashables())),
    )
    def test_intersection(self, set1, set2):
        set3 = set1 ^ set2
        assert type(set3) == type(set1) == type(set2)
