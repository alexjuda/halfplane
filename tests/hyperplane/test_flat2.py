import pytest
import numpy as np
import numpy.testing

from hyperplane import flat2


class TestLineLineIntersetion:
    @pytest.mark.parametrize(
        "a1,b1,a2,b2,x,y",
        [
            (1, 0, -2, 3, 1, 1),
            (1, 0, 2, 0, 0, 0),
            (3, 0, 2, 0, 0, 0),
            (-1, -1, 2, 2, -1, 0),
        ],
    )
    def test_crossing_lines(self, a1, b1, a2, b2, x, y):
        assert (
            list(
                flat2.line_line_intersection(
                    flat2.Line(a1, b1),
                    flat2.Line(a2, b2),
                )
            )
            == [x, y]
        )


class TestVertices:
    def test_triangle(self):
        shape = flat2.Triangle(
            (
                flat2.Halfplane(flat2.Line(1, 0), flat2.Op.GREATER_THAN),
                flat2.Halfplane(flat2.Line(2, 0), flat2.Op.LESS_THAN),
                flat2.Halfplane(flat2.Line(-1, 4), flat2.Op.LESS_THAN),
            )
        )
        np.testing.assert_array_almost_equal(
            shape.vertices,
            [
                [0, 0],
                [2, 2],
                [1.3333333, 2.6666666],
            ],
        )
