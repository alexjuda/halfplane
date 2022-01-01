from hyperplane.v4 import flat
import pytest

HP_EXAMPLES = [
    # --- vertical line ---
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(1, 2)),
    # point outside the segment boundary
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(1, 6)),
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(1, -1)),
    # --- horizontal line ---
    (flat.Pt(1, 1), flat.Pt(4, 1), flat.Pt(2, -2)),
    # point on segment
    # (flat.Pt(1, 1), flat.Pt(4, 1), flat.Pt(2, 1)),
    # --- problematic samples ---
    #     B
    #  A     C
    # hp(AB) -> y <= x -> -x + y <= 0
    (flat.Pt(0, 0), flat.Pt(5, 5), flat.Pt(10, 0)),
]


HPC_EXAMPLES = [
    # --- vertical line ---
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(-1, 2)),
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(-1, -3)),
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(-1, 7)),
    # point on segment
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(0, 2)),
    # segment vertices
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(0, 1)),
    (flat.Pt(0, 1), flat.Pt(0, 4), flat.Pt(0, 4)),
    # --- horizontal line ---
    (flat.Pt(1, 1), flat.Pt(4, 1), flat.Pt(2, 2)),
    (flat.Pt(1, 1), flat.Pt(4, 1), flat.Pt(0, 2)),
    (flat.Pt(1, 1), flat.Pt(4, 1), flat.Pt(7, 2)),
    # --- top-right line ---
    (flat.Pt(1, 1), flat.Pt(4, 5), flat.Pt(0, 1)),
    (flat.Pt(1, 1), flat.Pt(4, 5), flat.Pt(0, 0)),
    # --- top-left line ---
    (flat.Pt(6, 1), flat.Pt(1, 5.5), flat.Pt(-0.01, 0)),
]


class TestHSContainsPt:
    @pytest.mark.parametrize("p1,p2,tested_point", HP_EXAMPLES)
    def test_hp_contains_point(self, p1, p2, tested_point):
        assert flat.Hp(p1, p2).contains(tested_point)

    @pytest.mark.parametrize("p1,p2,tested_point", HPC_EXAMPLES)
    def test_hpc_contains_point(self, p1, p2, tested_point):
        assert flat.Hpc(p1, p2).contains(tested_point)

    @pytest.mark.parametrize("p1,p2,tested_point", [*HP_EXAMPLES, *HPC_EXAMPLES])
    def test_point_is_either_in_hp_or_hpc(self, p1, p2, tested_point):
        hp = flat.Hp(p1, p2)
        hpc = flat.Hpc(p1, p2)

        assert hp.contains(tested_point) != hpc.contains(tested_point)
