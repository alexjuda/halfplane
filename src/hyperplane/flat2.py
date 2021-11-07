import abc
import typing as t
import enum

import numpy as np

from hyperplane.core import model, Coord


@model
class Line:
    a: Coord
    b: Coord


# class Circle:
#     r: Coord


Curve = t.Union[Line]


# Op = Enum(
#     "Op",
#     [
#         "LESS_THAN",
#         "GREATER_THAN",
#         "LESS_THAN_OR_EQUAL",
#         "GREATER_THAN_OR_EQUAL",
#     ],
# )


class Op(enum.Enum):
    LESS_THAN = enum.auto()
    GREATER_THAN = enum.auto()
    LESS_THAN_OR_EQUAL = enum.auto()
    GREATER_THAN_OR_EQUAL = enum.auto()


@model
class Halfplane:
    """A 2d halfspace cut out by a line.

    Represents all points on one side of a line.
    """

    line: Line
    op: Op


@model
class Triangle:
    halfplanes: t.Tuple[Halfplane, Halfplane, Halfplane]
    # TODO: add halfspace direction validation

    @property
    def vertices(self) -> np.ndarray:
        return line_intersections(hp.line for hp in self.halfplanes)


@model
class Rectangle:
    halfplanes: t.Tuple[Halfplane, Halfplane, Halfplane, Halfplane]
    # TODO: add halfspace direction validation


def line_intersections(lines: t.Iterable[Line]):
    line_list = list(lines)
    intersections = []
    for line1_i in range(len(line_list)):
        line1 = line_list[line1_i]

        for line2_i in range(line1_i + 1, len(line_list)):
            line2 = line_list[line2_i]

            try:
                point = line_line_intersection(line1, line2)
            except ValueError:
                continue

            intersections.append(point)
    return np.vstack(intersections)


def line_line_intersection(line1: Line, line2: Line):
    if line1.a == line2.a:
        raise ValueError("There's no intersection for parallel lines")

    x = (line2.b - line1.b) / (line1.a - line2.a)
    y = line1.a * x + line1.b
    return np.array([x, y])
