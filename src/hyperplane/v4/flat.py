import typing as t

from hyperplane.core import Coord


class Pt(t.NamedTuple):
    x: Coord
    y: Coord


class Hp(t.NamedTuple):
    p1: Pt
    p2: Pt


class Hpc(t.NamedTuple):
    p1: Pt
    p2: Pt
