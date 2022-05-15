import dataclasses

import pytest

from hyperplane.flat import (
    X,
    XSegment,
    Esum,
    Hp,
    Hpc,
    Pt,
    collapse_xs,
    infer_smallest_segments,
)


def _translate_point(pt: Pt, dx, dy):
    return Pt(pt.x + dx, pt.y + dy)


class TestHSContainsPt:
    HP_POINT_EXAMPLES = [
        # --- vertical line ---
        (Pt(0, 4), Pt(0, 1), Pt(1, 2)),
        # point outside the segment boundary
        (Pt(0, 4), Pt(0, 1), Pt(1, 6)),
        (Pt(0, 4), Pt(0, 1), Pt(1, -1)),
        # --- horizontal line ---
        (Pt(4, 1), Pt(1, 1), Pt(2, -2)),
        # point on segment
        # (Pt(1, 1), Pt(4, 1), Pt(2, 1)),
        # --- problematic samples ---
        #     B
        #  A     C
        # hp(AB) -> y <= x -> -x + y <= 0
        (Pt(5, 5), Pt(0, 0), Pt(10, 0)),
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
        # --- numerical errors ---
        # FIXME: this point is not considered a part of the halfspace that
        # produced it when intersected with another halfspace.
        # (Pt(8, 10), Pt(4, 2), Pt(9.333333333333334, 12.666666666666668)),
        # (Pt(12, 2), Pt(10, 10), Pt(9.333333333333334, 12.666666666666668)),
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
        hpc = Hpc(p2, p1)

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
                {frozenset([Hp(Pt(0, 4), Pt(0, 1))])},
                # horizontal line
                {frozenset([Hp(Pt(2, 7), Pt(2, 2))])},
                {
                    frozenset([Hp(Pt(0, 4), Pt(0, 1))]),
                    frozenset([Hp(Pt(2, 7), Pt(2, 2))]),
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
                {frozenset([Hp(Pt(0, 4), Pt(0, 1))])},
                # horizontal line
                {frozenset([Hp(Pt(2, 7), Pt(2, 2))])},
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
                {frozenset([Hp(Pt(0, 4), Pt(0, 1))])},
                # horizontal line
                {frozenset([Hp(Pt(2, 7), Pt(2, 2))])},
                {frozenset([Hp(Pt(0, 4), Pt(0, 1)), Hp(Pt(2, 7), Pt(2, 2))])},
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
            {frozenset([Hpc(Pt(0, 4), Pt(0, 1))])},
        ),
        (
            # single vertical halfplane
            {frozenset([Hpc(Pt(0, 1), Pt(0, 4))])},
            {frozenset([Hp(Pt(0, 4), Pt(0, 1))])},
        ),
        (
            # vertical halfplane + horizontal halfplane
            {
                frozenset([Hp(Pt(0, 4), Pt(0, 1))]),
                frozenset([Hp(Pt(6, 1), Pt(-2, 1))]),
            },
            {
                frozenset([Hpc(Pt(0, 1), Pt(0, 4)), Hpc(Pt(-2, 1), Pt(6, 1))]),
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


class TestHsIntersection:
    HS_POINT_EXAMPLES = [
        (
            # horizontal line (-)
            Hp(Pt(0, 1), Pt(4, 1)),
            # diagonal line (/)
            Hp(Pt(2, 0), Pt(4, 4)),
            Pt(2.5, 1),
        ),
        (
            # diagonal line (\)
            Hp(Pt(1, 8), Pt(5, 0)),
            # diagonal line (/)
            Hp(Pt(2, 0), Pt(4, 4)),
            Pt(3.5, 3),
        ),
        (
            # horizontal line (-)
            Hp(Pt(0, 1), Pt(4, 1)),
            # vertical line (|)
            Hp(Pt(2, 0), Pt(2, 10)),
            Pt(2, 1),
        ),
        (
            # horizontal line (-)
            Hp(Pt(0, 1), Pt(4, 1)),
            # horizontal line (-)
            Hp(Pt(10, -1), Pt(14, -1)),
            None,
        ),
        (
            # vertical line (|)
            Hp(Pt(-1, 0), Pt(-1, -10)),
            # vertical line (|)
            Hp(Pt(10, 0), Pt(10, 10)),
            None,
        ),
    ]

    HS_HS_EXAMPLES = [(hs1, hs2) for hs1, hs2, _ in HS_POINT_EXAMPLES]

    @pytest.mark.parametrize("hs1,hs2,expected_point", HS_POINT_EXAMPLES)
    def test_examples(self, hs1, hs2, expected_point):
        assert X(hs1, hs2).point == expected_point

    @pytest.mark.parametrize("hs1,hs2", HS_HS_EXAMPLES)
    def test_order_invariance(self, hs1, hs2):
        assert X(hs1, hs2).point == X(hs2, hs1).point

    @pytest.mark.parametrize("hs1,hs2", HS_HS_EXAMPLES)
    def test_conjugate_invariance(self, hs1, hs2):
        assert X(hs1, hs2).point == X(hs1.conjugate, hs2).point
        assert X(hs1, hs2).point == X(hs1, hs2.conjugate).point
        assert (
            X(hs1, hs2).point
            == X(hs1.conjugate, hs2.conjugate).point
        )

    @pytest.mark.parametrize("hs1,hs2", HS_HS_EXAMPLES)
    def test_self(self, hs1, hs2):
        assert X(hs1, hs1).point is None
        assert X(hs2, hs2).point is None


@pytest.mark.parametrize(
    "bx",
    [
        X(
            Hp(Pt(-1, 0), Pt(-1, -10)),
            Hp(Pt(10, 0), Pt(10, 10)),
        )
    ],
)
class TestCollapsingBoundCrosses:
    def test_is_equal_to_itself(self, bx):
        assert collapse_xs([bx, bx]) == [bx]

    def test_not_equal_when_moving_points(self, bx):
        p1 = bx.hs2.p1
        new_p1 = Pt(p1.x + 1, p1.y + 2)
        bx2 = X(bx.hs1, dataclasses.replace(bx.hs2, p1=new_p1))

        assert collapse_xs([bx, bx2]) == [bx, bx2]

    def test_is_equal_to_reversed_hses(self, bx):
        bx2 = X(bx.hs2, bx.hs1)
        assert collapse_xs([bx, bx2]) == [bx]


class TestDebugNames:
    @pytest.mark.parametrize(
        "obj",
        [
            Pt(-1, 1),
            Hp(Pt(10, 0), Pt(10, 10)),
            Hpc(Pt(10, 0), Pt(10, 10)),
            X(
                Hp(Pt(-1, 0), Pt(-1, -10)),
                Hp(Pt(10, 0), Pt(10, 10)),
            ),
        ],
    )
    class TestForAllTypeExamples:
        def test_equals_despite_different_names(self, obj):
            assert (
                obj
                == dataclasses.replace(obj, debug_name=None)
                == dataclasses.replace(obj, debug_name="hurrdurr")
            )

        def test_hash_despite_different_names(self, obj):
            assert (
                hash(obj)
                == hash(dataclasses.replace(obj, debug_name=None))
                == hash(dataclasses.replace(obj, debug_name="hurrdurr"))
            )

    @pytest.mark.parametrize(
        "root_obj,root_attr",
        [
            (Hp(Pt(10, 0), Pt(10, 10)), "p1"),
            (Hpc(Pt(10, 0), Pt(10, 10)), "p1"),
            (
                X(
                    Hp(Pt(-1, 0), Pt(-1, -10)),
                    Hp(Pt(10, 0), Pt(10, 10)),
                ),
                "hs1",
            ),
        ],
    )
    def test_nested_object(self, root_obj, root_attr):
        old_nested = getattr(root_obj, root_attr)
        new_nested = dataclasses.replace(old_nested, debug_name="hello")
        new_root = dataclasses.replace(root_obj, **{root_attr: new_nested})
        assert new_root == root_obj


class TestInferSegments:
    @pytest.fixture
    def h0(self):
        return Hpc(
            p1=Pt(x=2, y=6, debug_name="p_17"),
            p2=Pt(x=6, y=2, debug_name="p_17"),
            debug_name="h_0",
        )

    @pytest.fixture
    def x13(self, h0):
        return X(
            hs1=Hp(
                p1=Pt(x=10, y=4, debug_name="p_17"),
                p2=Pt(x=6, y=4, debug_name="p_17"),
                debug_name="h_9",
            ),
            hs2=h0,
            debug_name="x_13",
        )

    @pytest.fixture
    def x0(self, h0):
        return X(
            hs1=h0,
            hs2=Hp(
                p1=Pt(x=4, y=0, debug_name="p_17"),
                p2=Pt(x=4, y=10, debug_name="p_17"),
                debug_name="h_8",
            ),
            debug_name="x_0",
        )

    @pytest.fixture
    def x4(self, h0):
        return X(
            hs1=h0,
            hs2=Hpc(
                p1=Pt(x=2, y=10, debug_name="p_17"),
                p2=Pt(x=2, y=0, debug_name="p_17"),
                debug_name="h_5",
            ),
            debug_name="x_4",
        )

    @pytest.fixture
    def x2(self, h0):
        return X(
            hs1=Hpc(
                p1=Pt(x=6, y=2, debug_name="p_17"),
                p2=Pt(x=10, y=2, debug_name="p_17"),
                debug_name="h_6",
            ),
            hs2=h0,
            debug_name="x_2",
        )

    @pytest.fixture
    def xs_problematic(self, h0, x13, x0, x4, x2):
        return [x13, x0, x4, x2]

    @pytest.fixture
    def problematic_ref_segments(self, h0, x13, x0, x4, x2):
        return [
            XSegment(x4, x13),
            XSegment(x13, x0),
            XSegment(x0, x2),
        ]

    def test_examples(self, xs_problematic, h0, problematic_ref_segments):
        segments = infer_smallest_segments(xs_problematic, h0)
        assert segments == problematic_ref_segments
