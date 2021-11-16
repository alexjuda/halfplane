import typing as t
from hyperplane.core import Coord


class Point(t.NamedTuple):
    x: Coord
    y: Coord


class Segment(t.NamedTuple):
    """Line constrained by points, with direction.

    Consider an example:
    - AB = ((5, 1), (9, 5))
    - DC = ((19, 5), (15, 1))
    - DB = ((19, 5), (9, 5))

         ▲
         │             ▲
        5┼        B────┴────D
         │       /         /
         │      /─►     ◄─/
         │     /         /
        1┼    A         C
       ──┼────┼───┼─────┼───┼──►
         │              1   1
         │    5   9     5   9
    """

    p1: Point
    p2: Point

    # If true, the halfplane represented by this segment should not include the boundary
    # line.
    strict: bool = False


def segments_intersect(s1: Segment, s2: Segment) -> bool:
    """Based on:
    https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
    """
    # P1 = (x1, y1)
    # P2 = (x2, y2)
    # P3 = (x3, y3)
    # P4 = (x4, y4)
    #
    # S1 = (P1, P2) = ((x1, y1), (x2, y2))
    # S2 = (P3, P4) = ((x3, y3), (x4, y4))

    dx12 = s1.p1.x - s1.p2.x
    dx13 = s1.p1.x - s2.p1.x
    dx34 = s2.p1.x - s2.p2.x

    dy12 = s1.p1.y - s1.p2.y
    dy13 = s1.p1.y - s2.p1.y
    dy34 = s2.p1.y - s2.p2.y

    denominator = dx12 * dy34 - dy12 * dx34

    t = (dx13 * dy34 - dy13 * dx34) / denominator
    u = (dx13 * dy12 - dy12 * dx12) / denominator

    return 0 <= t <= 1 and 0 <= u <= 1
