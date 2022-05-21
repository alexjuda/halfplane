from hyperplane import flat, common_shapes
from hyperplane.flat import Pt, Hpc, X, XSegment

import pytest


def _triangle_boundary():
    return [
        XSegment(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10)),
            ),
        ),
        XSegment(
            x1=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1)),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10)),
            ),
        ),
        XSegment(
            x1=X(
                hs1=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1)),
                hs2=Hpc(p1=Pt(x=9, y=1), p2=Pt(x=4, y=10)),
            ),
            x2=X(
                hs1=Hpc(p1=Pt(x=2, y=2), p2=Pt(x=10, y=2)),
                hs2=Hpc(p1=Pt(x=8, y=10), p2=Pt(x=3, y=1)),
            ),
        ),
    ]


@pytest.mark.parametrize(
    "esum,expected_segments",
    [
        (common_shapes.triangle(), _triangle_boundary()),
    ],
)
def test_detect_boundary(esum, expected_segments):
    segments = flat.detect_boundary(esum)
    assert segments == expected_segments
