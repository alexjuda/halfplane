from hyperplane.v4 import flat
import pytest


class TestHSContainsPt:
    POSITIVE_EXAMPLES = [
        # --- vertical line ---
        (flat.Hp(flat.Pt(0, 1), flat.Pt(0, 4)), flat.Pt(1, 2)),
        # point on segment
        # (flat.Hp(flat.Pt(0, 1), flat.Pt(0, 4)), flat.Pt(0, 2)),
        # point outside the segment boundary
        (flat.Hp(flat.Pt(0, 1), flat.Pt(0, 4)), flat.Pt(1, 6)),
        (flat.Hp(flat.Pt(0, 1), flat.Pt(0, 4)), flat.Pt(1, -1)),
        # segment vertices
        # (flat.Hp(flat.Pt(0, 1), flat.Pt(0, 4)), flat.Pt(0, 1)),
        # (flat.Hp(flat.Pt(0, 1), flat.Pt(0, 4)), flat.Pt(0, 4)),
        # --- horizontal line ---
        (flat.Hp(flat.Pt(1, 1), flat.Pt(4, 1)), flat.Pt(2, -2)),
        # point on segment
        # (flat.Hp(flat.Pt(1, 1), flat.Pt(4, 1)), flat.Pt(2, 1)),
        # --- problematic samples ---
        #     B
        #  A     C
        # hp(AB) -> y <= x -> -x + y <= 0
        (flat.Hp(flat.Pt(0, 0), flat.Pt(5, 5)), flat.Pt(10, 0)),
    ]

    @pytest.mark.parametrize("hs,point", POSITIVE_EXAMPLES)
    def test_positive(self, hs, point):
        assert flat.contains_point(hs, point)
