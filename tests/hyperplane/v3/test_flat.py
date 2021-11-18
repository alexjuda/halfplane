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
            # TODO: fix this case
            # (
            #     flat.Segment(flat.Point(0, 4), flat.Point(4, 4)),
            #     flat.Segment(flat.Point(3, 4), flat.Point(6, 4)),
            #     True,
            #     "collinear-overlapping",
            # ),
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


class TestHalfplane:
    POSITIVE_EXAMPLES = [
        # --- vertical line ---
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(1, 2)),
        # point on segment
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(0, 2)),
        # point outside the segment boundary
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(1, 6)),
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(1, -1)),
        # segment vertices
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(0, 1)),
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(0, 4)),
        # --- horizontal line ---
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 1)), flat.Point(2, -2)),
        # point on segment
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 1)), flat.Point(2, 1)),
    ]

    @pytest.mark.parametrize("segment,point", POSITIVE_EXAMPLES)
    def test_positive(self, segment, point):
        hp = flat.Halfplane.from_segment(segment)
        assert hp.contains_point(point)

    NEGATIVE_EXAMPLES = [
        # --- vertical line ---
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(-1, 2)),
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(-1, -3)),
        (flat.Segment(flat.Point(0, 1), flat.Point(0, 4)), flat.Point(-1, 7)),
        # --- horizontal line ---
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 1)), flat.Point(2, 2)),
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 1)), flat.Point(0, 2)),
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 1)), flat.Point(7, 2)),
        # --- top-right line ---
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 5)), flat.Point(0, 1)),
        (flat.Segment(flat.Point(1, 1), flat.Point(4, 5)), flat.Point(0, 0)),
        # --- top-left line ---
        (flat.Segment(flat.Point(6, 1), flat.Point(1, 5.5)), flat.Point(-0.01, 0)),
    ]

    @pytest.mark.parametrize("segment,point", NEGATIVE_EXAMPLES)
    def test_negative(self, segment, point):
        hp = flat.Halfplane.from_segment(segment)
        assert not hp.contains_point(point)

    @pytest.mark.parametrize("segment,point", NEGATIVE_EXAMPLES)
    def test_negative_is_positive_after_flipping(self, segment, point):
        hp = flat.Halfplane.from_segment(flat.Segment(segment.p2, segment.p1))
        assert hp.contains_point(point)
