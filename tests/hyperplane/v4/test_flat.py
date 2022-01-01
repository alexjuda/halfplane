from hyperplane.v4.flat import Pt, Hp, Hpc, Esum
import pytest


class TestHSContainsPt:
    HP_EXAMPLES = [
        # --- vertical line ---
        (Pt(0, 1), Pt(0, 4), Pt(1, 2)),
        # point outside the segment boundary
        (Pt(0, 1), Pt(0, 4), Pt(1, 6)),
        (Pt(0, 1), Pt(0, 4), Pt(1, -1)),
        # --- horizontal line ---
        (Pt(1, 1), Pt(4, 1), Pt(2, -2)),
        # point on segment
        # (Pt(1, 1), Pt(4, 1), Pt(2, 1)),
        # --- problematic samples ---
        #     B
        #  A     C
        # hp(AB) -> y <= x -> -x + y <= 0
        (Pt(0, 0), Pt(5, 5), Pt(10, 0)),
    ]

    HPC_EXAMPLES = [
        # --- vertical line ---
        (Pt(0, 1), Pt(0, 4), Pt(-1, 2)),
        (Pt(0, 1), Pt(0, 4), Pt(-1, -3)),
        (Pt(0, 1), Pt(0, 4), Pt(-1, 7)),
        # point on segment
        (Pt(0, 1), Pt(0, 4), Pt(0, 2)),
        # segment vertices
        (Pt(0, 1), Pt(0, 4), Pt(0, 1)),
        (Pt(0, 1), Pt(0, 4), Pt(0, 4)),
        # --- horizontal line ---
        (Pt(1, 1), Pt(4, 1), Pt(2, 2)),
        (Pt(1, 1), Pt(4, 1), Pt(0, 2)),
        (Pt(1, 1), Pt(4, 1), Pt(7, 2)),
        # --- top-right line ---
        (Pt(1, 1), Pt(4, 5), Pt(0, 1)),
        (Pt(1, 1), Pt(4, 5), Pt(0, 0)),
        # --- top-left line ---
        (Pt(6, 1), Pt(1, 5.5), Pt(-0.01, 0)),
    ]

    @pytest.mark.parametrize("p1,p2,tested_point", HP_EXAMPLES)
    def test_hp_contains_point(self, p1, p2, tested_point):
        assert Hp(p1, p2).contains(tested_point)

    @pytest.mark.parametrize("p1,p2,tested_point", HPC_EXAMPLES)
    def test_hpc_contains_point(self, p1, p2, tested_point):
        assert Hpc(p1, p2).contains(tested_point)

    @pytest.mark.parametrize("p1,p2,tested_point", [*HP_EXAMPLES, *HPC_EXAMPLES])
    def test_point_is_either_in_hp_or_hpc(self, p1, p2, tested_point):
        hp = Hp(p1, p2)
        hpc = Hpc(p1, p2)

        assert hp.contains(tested_point) != hpc.contains(tested_point)


class TestMergingEsum:
    @pytest.mark.parametrize(
        "terms1,terms2,expected_terms",
        [
            (set(), set(), set()),
            (
                # vertical line
                {frozenset([Hp(Pt(0, 1), Pt(0, 4))])},
                # horizontal line
                {frozenset([Hp(Pt(2, 2), Pt(2, 7))])},
                {
                    frozenset([Hp(Pt(0, 1), Pt(0, 4))]),
                    frozenset([Hp(Pt(2, 2), Pt(2, 7))]),
                },
            ),
        ],
    )
    def test_union_examples(self, terms1, terms2, expected_terms):
        esum1 = Esum(terms1)
        esum2 = Esum(terms2)
        assert esum1.union(esum2).terms == expected_terms

    @pytest.mark.parametrize(
        "terms1,terms2",
        [
            (set(), set()),
            (
                # vertical line
                {frozenset([Hp(Pt(0, 1), Pt(0, 4))])},
                # horizontal line
                {frozenset([Hp(Pt(2, 2), Pt(2, 7))])},
            ),
        ],
    )
    def test_union_is_superset(self, terms1, terms2):
        esum1 = Esum(terms1)
        esum2 = Esum(terms2)
        combined = esum1.union(esum2)

        assert combined.terms.issuperset(terms1)
        assert combined.terms.issuperset(terms2)

    @pytest.mark.parametrize(
        "terms1,terms2,expected_terms",
        [
            (set(), set(), set()),
            (
                # vertical line
                {frozenset([Hp(Pt(0, 1), Pt(0, 4))])},
                # horizontal line
                {frozenset([Hp(Pt(2, 2), Pt(2, 7))])},
                {frozenset([Hp(Pt(0, 1), Pt(0, 4)), Hp(Pt(2, 2), Pt(2, 7))])},
            ),
        ],
    )
    def test_intersection_examples(self, terms1, terms2, expected_terms):
        esum1 = Esum(terms1)
        esum2 = Esum(terms2)
        assert esum1.intersection(esum2).terms == expected_terms
