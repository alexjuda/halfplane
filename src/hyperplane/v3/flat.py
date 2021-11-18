import abc
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

    t_numerator = dx13 * dy34 - dy13 * dx34
    u_numerator = dx13 * dy12 - dy12 * dx12

    denominator = dx12 * dy34 - dy12 * dx34

    if denominator == 0:
        # This probably means the segments are collinear
        # TODO: detect if segments overlap
        return False

    t = t_numerator / denominator
    u = u_numerator / denominator

    return 0 <= t <= 1 and 0 <= u <= 1


# class HasSegments:
#     @abc.abstractproperty
#     def segments(self) -> t.Sequence[Segment]:
#         ...


# class ContainsSegmentMixin(HasSegments):
#     def contains_segment(self, segment: Segment) -> bool:
#         pass
#         # self.segments


class Container(abc.ABC):
    @abc.abstractmethod
    def contains_point(self, point: Point) -> bool:
        pass


class Polygon(Container):
    def __init__(self, vertices: t.Sequence[Point]):
        """
        Args:
            points: sequence of points. Order matters!
        """
        if len(vertices) < 3:
            raise ValueError(f"Polygon needs at least 3 vertices. Got: {vertices}")

        self._vertices = vertices

    @property
    def segments(self):
        return [
            *(
                Segment(self._vertices[i], self._vertices[i + 1])
                for i in range(len(self._vertices) - 1)
            ),
            Segment(self._vertices[-1], self._vertices[0]),
        ]

    def contains_point(self, point: Point):
        pass


class Halfplane(Container):
    def __init__(self, a: Coord, b: Coord, c: Coord):
        """
        Representation of a halfplane using an inequality based on Carthesian plane
        coordinates:
            L = {(x, y) | ax + by = c}

        The inequality is `ax + by ≤ c`
        """
        self._a = a
        self._b = b
        self._c = c

    def contains_point(self, point: Point) -> bool:
        return self._a * point.x + self._b * point.y <= self._c

    @classmethod
    def from_segment(cls, segment: Segment) -> "Halfplane":
        """Treats a segment like it was a line. Figures out the inequality direction
        based on the segment direction.
        """
        # ax1 + by1 = c
        # ax2 + by2 = c
        # ax + by = c
        # by = ax + c
        # y = ax/b + c/b
        # m = (y2 - y1) / (x2 - x1)
        # m = a/b

        if segment.p1.x == segment.p2.x:
            # vertical line
            # b = 0
            # ax ≤ c
            # a = 1 | a = -1
            # x ≤ c | x ≤ -c
            if segment.p1.y < segment.p2.y:
                # x ≥ x1 = x2
                # -x + 0y ≤ -x1 = - x2
                return Halfplane(-1, 0, -segment.p1.x)
            else:
                # x ≤ x1 = x2
                # x + 0y ≤ x1 = x2
                return Halfplane(1, 0, segment.p1.x)

        # ax + by ≤ c
        # by ≤ ax + c
        # b = 1
        # y ≤ ax + c
        # y - ax ≤ c
        m = (segment.p2.y - segment.p1.y) / (segment.p2.x - segment.p1.x)
        y0 = segment.p1.y - m * segment.p1.x

        # Motivation: we're looking at the diff vector to determine the sign of the
        # inequality. If the diff vector points more to the left than to the right then:
        # - the segment normal will point upwards
        # - the inequality is y ≥ mx + y0
        # - we have to invert the coefficients
        dx = segment.p2.x - segment.p1.x
        if dx < 0:
            return Halfplane(m, -1, -y0)
        else:
            return Halfplane(m, 1, y0)


def triangle(p1: Point, p2: Point, p3: Point) -> Polygon:
    # We need to figure out the segment direction.
    # 1. Start with p1
    # 2. Select p2 or p3 as the next one
    # 3. Add the remaining one
    # 4. Go back to p1
    #
    # Scenario 1. Valid sequence: ABC
    #
    #   B
    #            C
    #
    #     A
    #
    #
    # Scenario 1. Valid sequence: ACB
    #
    #   C
    #            B
    #
    #     A
    #
    points = [p1]

    # middl
    return points
