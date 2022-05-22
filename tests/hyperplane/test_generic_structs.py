from hyperplane import generic_structs
import hypothesis as h
import hypothesis.strategies as st


class TestFrozenOrderedSet:
    @h.given(items=st.lists(st.integers()))
    def test_equal_to_plain_set(self, items):
        plain_set = set(items)

        o_set = generic_structs.FrozenOrderedSet(items)
        assert o_set == plain_set

    @h.given(items=st.lists(st.integers(), unique=True))
    def test_retains_order(self, items):
        o_set = generic_structs.FrozenOrderedSet(items)
        assert list(o_set) == items
