import pytest

from hyperplane.v3 import flat


class TestSegmentsIntersect:
    @pytest.mark.parametrize(
        "s1,s2,expected,description",
        [
            (
                flat.Segment(flat.Point(0, 4), flat.Point(4, 4)),
                flat.Segment(flat.Point(2, 0), flat.Point(2, 6)),
                True,
                "simple-cross",
            ),
            (
                flat.Segment(flat.Point(0, 4), flat.Point(0, 4)),
                flat.Segment(flat.Point(2, 0), flat.Point(2, 1)),
                False,
                "simple-cross-but-the-vertical-too-short",
            ),
            (
                flat.Segment(flat.Point(0, 4), flat.Point(0, 4)),
                flat.Segment(flat.Point(2, 0), flat.Point(2, 6)),
                False,
                "one-segment-has-0-length",
            ),
            (
                flat.Segment(flat.Point(0, 4), flat.Point(4, 4)),
                flat.Segment(flat.Point(4, 4), flat.Point(6, 4)),
                False,
                "collinear-adjacent",
            ),
            (
                flat.Segment(flat.Point(0, 4), flat.Point(4, 4)),
                flat.Segment(flat.Point(5, 4), flat.Point(6, 4)),
                False,
                "collinear-non-adjacent",
            ),
            (
                flat.Segment(flat.Point(0, 4), flat.Point(4, 4)),
                flat.Segment(flat.Point(3, 4), flat.Point(6, 4)),
                True,
                "collinear-overlapping",
            ),
            (
                flat.Segment(flat.Point(0, 4), flat.Point(4, 4)),
                flat.Segment(flat.Point(4, 4), flat.Point(4, 8)),
                True,
                "orthogonal-with-touchpoint",
            ),
        ],
    )
    def test_examples(self, s1, s2, expected, description):
        assert flat.segments_intersect(s1, s2) is expected
        assert flat.segments_intersect(s2, s1) is expected
        assert (
            flat.segments_intersect(
                flat.Segment(s1.p2, s1.p1),
                flat.Segment(s2.p2, s2.p1),
            )
            is expected
        )
        assert (
            flat.segments_intersect(
                flat.Segment(s2.p2, s2.p1),
                flat.Segment(s1.p2, s1.p1),
            )
            is expected
        )
