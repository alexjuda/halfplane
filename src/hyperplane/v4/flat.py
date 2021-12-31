import typing as t

from hyperplane.core import Coord


# Data structures needed:
# - [x] pt
# - [x] hP
# - [x] hPC
# - [ ] Esum
# - [ ] segment

# Operations needed:
# - [ ] hP contains pt?
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


class Hp(t.NamedTuple):
    p1: Pt
    p2: Pt


class Hpc(t.NamedTuple):
    p1: Pt
    p2: Pt
