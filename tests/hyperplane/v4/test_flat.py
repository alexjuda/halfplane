from hyperplane.v4.flat import Pt, Hp, Hpc, Esum
import pytest


def _translate_point(pt: Pt, dx, dy):
    return Pt(pt[0] + dx, pt[1] + dy)


class TestHSContainsPt:
    HP_POINT_EXAMPLES = [
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

    HPC_POINT_EXAMPLES = [
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

    @pytest.mark.parametrize("p1,p2,tested_point", HP_POINT_EXAMPLES)
    def test_hp_contains_point(self, p1, p2, tested_point):
        assert Hp(p1, p2).contains(tested_point)

    @pytest.mark.parametrize("p1,p2,tested_point", HPC_POINT_EXAMPLES)
    def test_hpc_contains_point(self, p1, p2, tested_point):
        assert Hpc(p1, p2).contains(tested_point)

    @pytest.mark.parametrize(
        "p1,p2,tested_point", [*HP_POINT_EXAMPLES, *HPC_POINT_EXAMPLES]
    )
    def test_point_is_either_in_hp_or_hpc(self, p1, p2, tested_point):
        hp = Hp(p1, p2)
        hpc = Hpc(p1, p2)

        assert hp.contains(tested_point) != hpc.contains(tested_point)

    @pytest.mark.parametrize(
        "p1,p2,tested_point", [*HP_POINT_EXAMPLES, *HPC_POINT_EXAMPLES]
    )
    def test_hp_conjugate_flips_content(self, p1, p2, tested_point):
        hp = Hp(p1, p2)
        assert hp.contains(tested_point) != hp.conjugate.contains(tested_point)

    @pytest.mark.parametrize(
        "p1,p2,tested_point", [*HP_POINT_EXAMPLES, *HPC_POINT_EXAMPLES]
    )
    def test_hpc_conjugate_flips_content(self, p1, p2, tested_point):
        hpc = Hp(p1, p2)
        assert hpc.contains(tested_point) != hpc.conjugate.contains(tested_point)

    @pytest.mark.parametrize(
        "p1,p2,tested_point", [*HP_POINT_EXAMPLES, *HPC_POINT_EXAMPLES]
    )
    @pytest.mark.parametrize("dx", [0, 10, -14])
    @pytest.mark.parametrize("dy", [0, 12, -25])
    @pytest.mark.parametrize("hs_class", [Hp, Hpc])
    def test_translation_invariance(self, hs_class, p1, p2, tested_point, dx, dy):
        original_contains = hs_class(p1, p2).contains(tested_point)
        translated_contains = hs_class(
            _translate_point(p1, dx, dy),
            _translate_point(p2, dx, dy),
        ).contains(_translate_point(tested_point, dx, dy))

        assert original_contains == translated_contains


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


class TestEsumConjugate:
    TERMS_CONJUGATED_EXAMPLES = [
        (set(), set()),
        (
            # single vertical halfplane
            {frozenset([Hp(Pt(0, 1), Pt(0, 4))])},
            {frozenset([Hpc(Pt(0, 1), Pt(0, 4))])},
        ),
        (
            # single vertical halfplane
            {frozenset([Hpc(Pt(0, 1), Pt(0, 4))])},
            {frozenset([Hp(Pt(0, 1), Pt(0, 4))])},
        ),
        (
            # vertical halfplane + horizontal halfplane
            {
                frozenset([Hp(Pt(0, 1), Pt(0, 4))]),
                frozenset([Hp(Pt(-2, 1), Pt(6, 1))]),
            },
            {
                frozenset([Hpc(Pt(0, 1), Pt(0, 4)), Hp(Pt(-2, 1), Pt(6, 1))]),
            },
        ),
    ]

    @pytest.mark.parametrize("terms,expected_terms", TERMS_CONJUGATED_EXAMPLES)
    def test_examples(self, terms, expected_terms):
        esum = Esum(terms)
        assert esum.conjugate.terms == expected_terms

    @pytest.mark.parametrize("terms", [term for term, _ in TERMS_CONJUGATED_EXAMPLES])
    def test_double_conjugate_is_nop(self, terms):
        esum = Esum(terms)
        assert esum.conjugate.conjugate == esum
