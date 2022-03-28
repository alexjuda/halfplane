import dataclasses
import typing as t
import itertools
import more_itertools
from numbers import Number
import math

import numpy as np

from .core import Coord


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
# - [x] point-by-point test


frozen_model = dataclasses.dataclass(frozen=True)


class IterableMixin:
    pass
    # def __iter__(self):
    #     return iter(dataclasses.astuple(self))

    # def __len__(self):
    #     return len(dataclasses.astuple(self))


@frozen_model
class Pt(IterableMixin):
    x: Coord
    y: Coord

    @property
    def position(self) -> np.ndarray:
        """3d position vector."""
        return np.array([self.x, self.y, 0])

    def distance(self, other: "Pt") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return math.hypot(dx, dy)


@frozen_model
class Hp(IterableMixin):
    """Half plane, where the boundary is a line that crosses p1 & p1. Doesn't
    include the boundary itself. Contains all points "on the left" of the
    P1->P2 vector.
    """

    p1: Pt
    p2: Pt

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) > 0

    @property
    def conjugate(self) -> "Hpc":
        return Hpc(self.p2, self.p1)

    def y(self, x: Number) -> t.Optional[Number]:
        return _extrapolate_line(self.p1, self.p2, x)


@frozen_model
class Hpc(IterableMixin):
    """Half plane, where the boundary is a line that crosses p1 & p1. Includes
    the boundary. Contains all points "on the left" of the P1->P2 vector.
    """

    p1: Pt
    p2: Pt

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) >= 0

    @property
    def conjugate(self) -> Hp:
        return Hp(self.p2, self.p1)

    def y(self, x: Number) -> t.Optional[Number]:
        return _extrapolate_line(self.p1, self.p2, x)


Hs = t.Union[Hp, Hpc]


def _z_factor(half_space: Hs, point: Pt) -> float:
    """Z coordinate of the cross product between the halfspace's vector and the
    position vector of the tested point.
    """
    p1, p2 = [p.position for p in [half_space.p1, half_space.p2]]
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


def _extrapolate_line(p1: Pt, p2: Pt, x: Number) -> t.Optional[Number]:
    if (line_params := _line_params(p1, p2)) is None:
        return None

    a, b = line_params

    return a * x + b


def _intersection_point(hs1: Hs, hs2: Hs) -> t.Optional[Pt]:
    # y = ax + b
    # a1 * x + b1 = a2 * x + b2
    # a1 * x - a2 * x + b1 = b2
    # a1 * x - a2 * x = b2 - b1
    # (a1 - a2) * x = b2 - b1
    # x = (b2 - b1) / (a1 - a2)
    # y = a1 * x + b1
    params1 = _line_params(hs1.p1, hs1.p2)
    params2 = _line_params(hs2.p1, hs2.p2)
    if params1 is None:
        if params2 is None:
            # Two vertical lines
            return None
        else:
            x = hs1.p1.x
            y = hs2.y(x)

            return Pt(x, y)
    elif params2 is None:
        return _intersection_point(hs2, hs1)

    a1, b1 = params1
    a2, b2 = params2

    if (delta_a := a1 - a2) == 0:
        return None

    # denominator is not zero unless the lines are parallel
    x = (b2 - b1) / delta_a
    y = a1 * x + b1

    return Pt(x, y)


# A group of intersecting halfspaces.
Term = t.Set[Hs]


@frozen_model
class Esum(IterableMixin):
    """Expression sum. Basic shape representation.

    Uses two-level sets of halfspaces. The outer set is considered a union of
    terms. The inner set (AKA a term) is considered an intersection of
    halfspaces.
    """

    terms: t.Set[Term]
    name: t.Optional[str] = None

    def union(self, other: "Esum") -> "Esum":
        return Esum(self.terms | other.terms)

    def intersection(self, other: "Esum") -> "Esum":
        new_terms = []
        for self_term in self.terms:
            for other_term in other.terms:
                new_terms.append(self_term ^ other_term)

        return Esum(frozenset(new_terms))

    def difference(self, other: "Esum") -> "Esum":
        return self.intersection(other.conjugate)

    def contains(self, point: Pt) -> bool:
        return any(all(hs.contains(point) for hs in term) for term in self.terms)

    @property
    def conjugate(self) -> "Esum":
        # I think the general pattern is like this:
        # 1. Start with Esum
        # 2. Generate Carthesian product of items in terms. Each generated
        #     tuple will be a term in the output Esum.
        # 3. Negate each item in each term.
        conjugate_terms = set()
        for product_term in itertools.product(*self.terms):
            conjugate_term = []
            for hs in product_term:
                conjugate_term.append(hs.conjugate)

            # Avoid empty inner sets
            if len(conjugate_term) > 0:
                conjugate_terms.add(frozenset(conjugate_term))

        return Esum(conjugate_terms)

    @property
    def with_boundaries(self) -> "Esum":
        return Esum(
            {frozenset(Hpc(hs.p1, hs.p2) for hs in term) for term in self.terms}
        )

    def contains_cross(self, cross: "BoundsCross") -> bool:
        """Checks if `cross` point is a member of this Esum. This includes
        crosspoints lying on the boundary, regardless of Hp/Hpc strictness.
        """
        # TODO: should the inner `all` be switched to an any?
        return any(
            all(_hs_contains_cross(hs, cross) for hs in term) for term in self.terms
        )


@frozen_model
class BoundsCross(IterableMixin):
    hs1: Hs
    hs2: Hs

    @property
    def point(self) -> Pt:
        return _intersection_point(self.hs1, self.hs2)

    @property
    def halfspaces(self) -> t.Sequence[Hs]:
        return [self.hs1, self.hs2]


def find_all_crosses(halfspaces: t.Iterable[Hs]) -> t.Set[BoundsCross]:
    return {
        cross
        for hs1, hs2 in itertools.combinations(halfspaces, 2)
        if (cross := BoundsCross(hs1, hs2)).point is not None
    }


def _hs_contains_cross(hs: Hs, cross: BoundsCross):
    # Check 1: see if `hs` was used to create this `cross`. This should
    # alleviate numerical errors.
    if hs in {cross.hs1, cross.hs2}:
        return True

    # Check 2: see if a `hs` contains the cross point. Allow points on
    # boundaries, even for `Hp`.
    return Hpc(hs.p1, hs.p2).contains(cross.point)


def find_vertices(esum: Esum) -> t.Set[BoundsCross]:
    crosses = find_all_crosses([hs for term in esum.terms for hs in term])
    inside = list(
        more_itertools.unique_everseen(
            cross for cross in crosses if esum.contains_cross(cross)
        )
    )
    collapsed = collapse_crosses(inside)
    return collapsed


def query_crosses(
    crosses: t.Iterable[BoundsCross], poi: Pt, eps: float = 0.1
) -> t.Iterable[BoundsCross]:
    return [x for x in crosses if x.point.distance(poi) < eps]


def query_cross(
    crosses: t.Iterable[BoundsCross], poi: Pt, eps: float = 0.1
) -> BoundsCross:
    results = query_crosses(crosses, poi, eps)
    assert len(results) == 1
    return results[0]


@frozen_model
class CrossSegment(IterableMixin):
    x1: BoundsCross
    x2: BoundsCross


def hs_crosses_index(
    crosses: t.Iterable[BoundsCross],
) -> t.Dict[Hs, t.Set[BoundsCross]]:
    """Cross maps from points to HSes. This maps from HSes to crosses."""
    index = {}
    for cross in crosses:
        for hs in [cross.hs1, cross.hs2]:
            index.setdefault(hs, set()).add(cross)
    return index


@frozen_model
class GraphEdge(IterableMixin):
    node1: t.Any
    node2: t.Any
    meta: t.Any


class Graph:
    def __init__(self, edges: t.Sequence[GraphEdge]):
        self.edges = set(edges)
        self._index = {
            node: edge for edge in edges for node in [edge.node1, edge.node2]
        }

    def edge_meta(self, node):
        return self._index[node].meta


class Glossary:
    def __init__(self, objs: t.Sequence, prefix: str):
        self._obj_name = {obj: f"{prefix}{obj_i}" for obj_i, obj in enumerate(objs)}
        self._name_obj = {name: obj for obj, name in self._obj_name.items()}

    def obj(self, name: str):
        return self._name_obj[name]

    def name(self, obj):
        return self._obj_name[obj]

    @property
    def dict(self):
        return self._name_obj


def segments(crosses: t.Iterable[BoundsCross]) -> t.Sequence[CrossSegment]:
    # - pick a vertex
    # - find both/all hses it crossed. Note: there might be duplicates if three
    #   lines intersect at the same point. Should we ignore this for now?
    # - for each hs, get all cross points. Note: we have a bipartite graph! Do
    #   we wanna go BFS or DFS? Is this a topological sort? It doesn't matter
    #   because we only care about the segments (graph edges), not about the
    #   segment order.
    # - make a new graph where edges are the segments. Traverse it. There might
    #   be cycles. Hopefully, yields a hull.
    cross_index = hs_crosses_index(crosses)

    edges = []
    for cross in crosses:
        for hs in [cross.hs1, cross.hs2]:
            for antipodal_cross in cross_index[hs]:
                # node 1 - cross
                # edge - hs
                # node 2 - intipodal cross
                edges.append(GraphEdge(node1=cross, node2=antipodal_cross, meta=hs))

    segment_graph = Graph(edges)

    return [CrossSegment(edge.node1, edge.node2) for edge in segment_graph.edges]


def collapse_crosses(crosses: t.Iterable[BoundsCross]) -> t.Sequence[BoundsCross]:
    """Filters out bound crosses that correspond to the same halfspace pairs."""
    seen_set = set()
    seen_inverted_set = set()
    filtered = []
    for cross in crosses:
        if cross in seen_set or cross in seen_inverted_set:
            continue

        seen_set.add(cross)
        seen_inverted_set.add(BoundsCross(cross.hs2, cross.hs1))
        filtered.append(cross)

    return filtered
