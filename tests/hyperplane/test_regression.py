import typing as t

from halfplane import flat, common_shapes
from halfplane.flat import Pt, Hp, Hpc, X, XSegment

import numpy as np
import numpy.testing
import pytest


def _triangle_boundary():
    return [
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2), debug_name="-"),
                hs2=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1), debug_name="/"),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2), debug_name="-"),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10), debug_name="\\"),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2), debug_name="-"),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10), debug_name="\\"),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1), debug_name="/"),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10), debug_name="\\"),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1), debug_name="/"),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10), debug_name="\\"),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2), debug_name="-"),
                hs2=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1), debug_name="/"),
            ),
        ),
    ]


def _crude_c_boundary():
    return [
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=12, y=10),
                    p2=Pt(x=-1, y=10),
                ),
                hs2=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=12, y=10),
                    p2=Pt(x=-1, y=10),
                ),
                hs2=Hpc(
                    p1=Pt(x=2, y=-1),
                    p2=Pt(x=2, y=12),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=1),
                    p2=Pt(x=11, y=1),
                ),
                hs2=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
                hs2=Hpc(
                    p1=Pt(x=12, y=2),
                    p2=Pt(x=-1, y=2),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=9),
                    p2=Pt(x=11, y=9),
                ),
                hs2=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=12, y=10),
                    p2=Pt(x=-1, y=10),
                ),
                hs2=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=1),
                    p2=Pt(x=11, y=1),
                ),
                hs2=Hpc(
                    p1=Pt(x=2, y=-1),
                    p2=Pt(x=2, y=12),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=1),
                    p2=Pt(x=11, y=1),
                ),
                hs2=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=9),
                    p2=Pt(x=11, y=9),
                ),
                hs2=Hpc(
                    p1=Pt(x=2, y=-1),
                    p2=Pt(x=2, y=12),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=9),
                    p2=Pt(x=11, y=9),
                ),
                hs2=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=9),
                    p2=Pt(x=11, y=9),
                ),
                hs2=Hpc(
                    p1=Pt(x=1, y=11),
                    p2=Pt(x=1, y=0),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=12, y=2),
                    p2=Pt(x=-1, y=2),
                ),
                hs2=Hpc(
                    p1=Pt(x=1, y=11),
                    p2=Pt(x=1, y=0),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=12, y=2),
                    p2=Pt(x=-1, y=2),
                ),
                hs2=Hpc(
                    p1=Pt(x=2, y=-1),
                    p2=Pt(x=2, y=12),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=0, y=9),
                    p2=Pt(x=11, y=9),
                ),
                hs2=Hpc(
                    p1=Pt(x=2, y=-1),
                    p2=Pt(x=2, y=12),
                ),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(
                    p1=Pt(x=10, y=0),
                    p2=Pt(x=10, y=11),
                ),
                hs2=Hpc(
                    p1=Pt(x=12, y=2),
                    p2=Pt(x=-1, y=2),
                ),
            ),
            x2=X(
                hs1=Hpc(
                    p1=Pt(x=12, y=2),
                    p2=Pt(x=-1, y=2),
                ),
                hs2=Hpc(
                    p1=Pt(x=2, y=-1),
                    p2=Pt(x=2, y=12),
                ),
            ),
        ),
    ]


def _letter_c_boundary():
    return [
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
                hs2=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
                hs2=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
                hs2=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=6, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=10, y=14), p2=Pt(x=6, y=14)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=10, y=14), p2=Pt(x=6, y=14)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=10, y=14), p2=Pt(x=6, y=14)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
                hs2=Hpc(p1=Pt(x=10, y=14), p2=Pt(x=6, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=6, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=10, y=14), p2=Pt(x=6, y=14)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=6, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hpc(p1=Pt(x=6, y=2), p2=Pt(x=10, y=2)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hpc(p1=Pt(x=6, y=2), p2=Pt(x=10, y=2)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=6, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
                hs2=Hpc(p1=Pt(x=10, y=14), p2=Pt(x=6, y=14)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
                hs2=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
                hs2=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
                hs2=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
                hs2=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
                hs2=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hpc(p1=Pt(x=6, y=14), p2=Pt(x=2, y=10)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=6, y=12), p2=Pt(x=10, y=12)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hp(p1=Pt(x=4, y=10), p2=Pt(x=8, y=14)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=10), p2=Pt(x=2, y=0)),
                hs2=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
                hs2=Hpc(p1=Pt(x=12, y=10), p2=Pt(x=12, y=14)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=8, y=2), p2=Pt(x=4, y=6)),
                hs2=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
            ),
        ),
        XSegment.from_xs(
            x1=X(
                hs1=Hp(p1=Pt(x=4, y=0), p2=Pt(x=4, y=10)),
                hs2=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
            ),
            x2=X(
                hs1=Hp(p1=Pt(x=10, y=4), p2=Pt(x=6, y=4)),
                hs2=Hpc(p1=Pt(x=2, y=6), p2=Pt(x=6, y=2)),
            ),
        ),
    ]


def _endpoints_arr(segments: t.Sequence[XSegment]) -> np.ndarray:
    """
    Returns:
        [n_segments x 4] array of endpoint coordinates
    """
    arr = np.zeros((len(segments), 4))

    for segment_i, segment in enumerate(segments):
        arr[segment_i, 0:2] = segment.x1.point.position2d
        arr[segment_i, 2:4] = segment.x2.point.position2d

    # We wanna make the comparisons independent on the order of segments.
    arr.sort(axis=0)

    return arr


@pytest.mark.parametrize(
    "esum,expected_segments",
    [
        (common_shapes.triangle(), _triangle_boundary()),
        (common_shapes.crude_c(), _crude_c_boundary()),
        (common_shapes.letter_c(), _letter_c_boundary()),
    ],
)
def test_detect_boundary(esum, expected_segments):
    segments = flat.detect_boundary(esum)
    np.testing.assert_array_almost_equal(
        _endpoints_arr(segments), _endpoints_arr(expected_segments)
    )
