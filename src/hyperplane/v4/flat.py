import typing as t

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
# - [ ] hP conjugate
# - [ ] hPC conjugate
# - [ ] Esum conjugate
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
    include the boundary itself. Contains all points "on the left" of the
    P1->P2 vector.
    """
    p1: Pt
    p2: Pt

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) < 0


class Hpc(t.NamedTuple):
    """Half plane, where the boundary is a line that crosses p1 & p1. Includes
    the boundary. Contains all points "on the right" of the P1->P2 vector.
    """
    p1: Pt
    p2: Pt

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) >= 0


Hs = t.Union[Hp, Hpc]


def _z_factor(half_space: Hs, point: Pt) -> float:
    """Z coordinate of the cross product between the halfspace's vector and the
    position vector of the tested point.
    """
    p1, p2 = [p.position for p in half_space]
    v_hs = p2 - p1
    v_test = point.position
    v_cross = np.cross(v_hs, v_test)

    return v_cross[-1]


Term = t.Set[Hs]


class Esum(t.NamedTuple):
    terms: t.Set[Term]

    def union(self, other: "Esum") -> "Esum":
        return Esum(self.terms | other.terms)

    def intersection(self, other: "Esum") -> "Esum":
        new_terms = []
        for self_term in self.terms:
            for other_term in other.terms:
                new_terms.append(self_term ^ other_term)

        return Esum(frozenset(new_terms))
