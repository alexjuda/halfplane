import typing as t
import itertools
from numbers import Number

import numpy as np

from hyperplane.core import Coord


# Data structures needed:
# - [x] pt
# - [x] hP
# - [x] hPC
# - [x] Esum
# - [ ] segment

# Operations needed:
# - [x] hP contains pt?
# - [x] hPC contains pt?
# - [x] merge two Esum with union
# - [x] merge two Esum with intersection
# - [x] hP conjugate
# - [x] hPC conjugate
# - [x] Esum conjugate
# - [ ] select intersecting segments

# Plotting:
# - [ ] point-by-point test


class Pt(t.NamedTuple):
    x: Coord
    y: Coord

    @property
    def position(self) -> np.ndarray:
        """3d position vector."""
        return np.array([*self, 0])


class Hp(t.NamedTuple):
    """Half plane, where the boundary is a line that crosses p1 & p1. Doesn't
    include the boundary itself. Contains all points "on the right" of the
    P1->P2 vector.
    """

    p1: Pt
    p2: Pt

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) < 0

    @property
    def conjugate(self) -> "Hpc":
        return Hpc(*self)

    def y(self, x: Number) -> t.Optional[Number]:
        return _extrapolate_line_y(*self, x)

    def x(self, y: Number) -> t.Optional[Number]:
        return _extrapolate_line_x(*self, y)


class Hpc(t.NamedTuple):
    """Half plane, where the boundary is a line that crosses p1 & p1. Includes
    the boundary. Contains all points "on the left" of the P1->P2 vector.
    """

    p1: Pt
    p2: Pt

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) >= 0

    @property
    def conjugate(self) -> Hp:
        return Hp(*self)

    def y(self, x: Number) -> t.Optional[Number]:
        return _extrapolate_line_y(*self, x)

    def x(self, y: Number) -> t.Optional[Number]:
        return _extrapolate_line_x(*self, y)


Hs = t.Union[Hp, Hpc]


def _z_factor(half_space: Hs, point: Pt) -> float:
    """Z coordinate of the cross product between the halfspace's vector and the
    position vector of the tested point.
    """
    p1, p2 = [p.position for p in half_space]
    v_hs = p2 - p1
    v_test = point.position - p1
    v_cross = np.cross(v_hs, v_test)

    return v_cross[-1]


def _line_params(point1: Pt, point2: Pt) -> t.Optional[t.Tuple[Number, Number]]:
    p1, p2 = [p.position for p in [point1, point2]]
    d = p2 - p1

    try:
        a = float(d[1]) / float(d[0])
    except ZeroDivisionError:
        return None

    b = p1[1] - a * p1[0]

    return a, b


def _extrapolate_line_y(p1: Pt, p2: Pt, x: Number) -> t.Optional[Number]:
    if (line_params := _line_params(p1, p2)) is None:
        return None

    a, b = line_params

    return a * x + b


def _extrapolate_line_x(p1: Pt, p2: Pt, y: Number) -> t.Optional[Number]:
    # y(x) = a * x + b
    # y = ax + b
    # y - b = ax
    # x(y) = (y - b) / a
    if (line_params := _line_params(p1, p2)) is None:
        return None

    a, b = line_params

    return (y - b) / a


# A group of intersecting halfspaces.
Term = t.Set[Hs]


class Esum(t.NamedTuple):
    """Expression sum. Basic shape representation.

    Uses two-level sets of halfspaces. The outer set is considered a union of
    terms. The inner set (AKA a term) is considered an intersection of
    halfspaces.
    """

    terms: t.Set[Term]

    def union(self, other: "Esum") -> "Esum":
        return Esum(self.terms | other.terms)

    def intersection(self, other: "Esum") -> "Esum":
        new_terms = []
        for self_term in self.terms:
            for other_term in other.terms:
                new_terms.append(self_term ^ other_term)

        return Esum(frozenset(new_terms))

    def contains(self, point: Pt) -> bool:
        return any(all(hs.contains(point) for hs in term) for term in self.terms)

    @property
    def conjugate(self) -> "Esum":
        # I think the general pattern is like this:
        # 1. Start with Esum
        # 2. Generate Carthesian product of items in terms. Each generated
        #     tuple will be a term in the output Esum.
        # 3. Negate each item in each term.
        conjugate_terms = []
        for product_term in itertools.product(*self.terms):
            conjugate_term = []
            for hs in product_term:
                conjugate_term.append(hs.conjugate)

            # Avoid empty inner sets
            if len(conjugate_term) > 0:
                conjugate_terms.append(frozenset(conjugate_term))

        return Esum(frozenset(conjugate_terms))
