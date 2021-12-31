import typing as t

import numpy as np

from hyperplane.core import Coord


# Data structures needed:
# - [x] pt
# - [x] hP
# - [x] hPC
# - [ ] Esum
# - [ ] segment

# Operations needed:
# - [x] hP contains pt?
# - [ ] hPC contains pt?
# - [ ] merge two Esum with union
# - [ ] merge two Esum with intersection
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
    def vector(self) -> np.ndarray:
        return np.array([*self, 0])


class Hp(t.NamedTuple):
    p1: Pt
    p2: Pt


class Hpc(t.NamedTuple):
    p1: Pt
    p2: Pt


Hs = t.Union[Hp, Hpc]


def contains_point(hs: Hs, pt: Pt) -> bool:
    p1, p2 = [p.vector for p in hs]
    v_hs = p2 - p1
    v_test = pt.vector
    v_cross = np.cross(v_hs, v_test)

    return v_cross[-1] < 0
