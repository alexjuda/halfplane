import dataclasses
import itertools
import math
import typing as t
from numbers import Number

import more_itertools as mitt
import numpy as np
from sortedcontainers import SortedDict, SortedSet

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
debug_name_field = dataclasses.field(
    default=None,
    hash=False,
    compare=False,
)


class TodoMixin:
    pass


@frozen_model
class Pt(TodoMixin):
    x: Coord
    y: Coord
    debug_name: t.Optional[str] = debug_name_field

    @property
    def position(self) -> np.ndarray:
        """3d position vector."""
        return np.array([self.x, self.y, 0])

    def distance(self, other: "Pt") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return math.hypot(dx, dy)


@frozen_model
class Hp(TodoMixin):
    """Half plane, where the boundary is a line that crosses p1 & p1. Doesn't
    include the boundary itself. Contains all points "on the left" of the
    P1->P2 vector.
    """

    p1: Pt
    p2: Pt
    debug_name: t.Optional[str] = debug_name_field

    def contains(self, point: Pt) -> bool:
        return _z_factor(self, point) > 0

    @property
    def conjugate(self) -> "Hpc":
        return Hpc(self.p2, self.p1)

    def y(self, x: Number) -> t.Optional[Number]:
        return _extrapolate_line(self.p1, self.p2, x)


@frozen_model
class Hpc(TodoMixin):
    """Half plane, where the boundary is a line that crosses p1 & p1. Includes
    the boundary. Contains all points "on the left" of the P1->P2 vector.
    """

    p1: Pt
    p2: Pt
    debug_name: t.Optional[str] = debug_name_field

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


@frozen_model
class Esum(TodoMixin):
    """Expression sum. Basic shape representation.

    Uses two-level sets of halfspaces. The outer set is considered a union of
    terms. The inner set (AKA a term) is considered an intersection of
    halfspaces.
    """

    # Each term is a group of intersecting halfspaces.
    terms: t.FrozenSet[t.FrozenSet[Hs]]
    name: t.Optional[str] = None
    debug_name: t.Optional[str] = debug_name_field

    def union(self, other: "Esum") -> "Esum":
        return Esum(self.terms | other.terms)

    def intersection(self, other: "Esum") -> "Esum":
        new_terms = []
        for self_term in self.terms:
            for other_term in other.terms:
                new_terms.append(self_term ^ other_term)

        return Esum(SortedSet(new_terms))

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
        conjugate_terms = SortedSet()
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
            SortedSet(
                frozenset(Hpc(hs.p1, hs.p2) for hs in term) for term in self.terms
            )
        )

    def contains_x(self, x: "X") -> bool:
        """Checks if cross point `x` is a member of this Esum. This includes
        crosspoints lying on the boundary, regardless of Hp/Hpc strictness.
        """
        # TODO: should the inner `all` be switched to an any?
        return any(all(_hs_contains_x(hs, x) for hs in term) for term in self.terms)


@frozen_model
class X(TodoMixin):
    """Cross point between two halspaces. Doesn't calculate coordinates until
    `point` is called.
    """

    hs1: Hs
    hs2: Hs
    debug_name: t.Optional[str] = debug_name_field

    @property
    def point(self) -> Pt:
        return _intersection_point(self.hs1, self.hs2)

    @property
    def halfspaces(self) -> t.Sequence[Hs]:
        return [self.hs1, self.hs2]


def find_all_xs(hses: t.Iterable[Hs]) -> t.Set[X]:
    return {
        x
        for hs1, hs2 in itertools.combinations(hses, 2)
        if (x := X(hs1, hs2)).point is not None
    }


def _hs_contains_x(hs: Hs, x: X):
    # Check 1: see if `hs` was used to create this `cross`. This should
    # alleviate numerical errors.
    if hs in {x.hs1, x.hs2}:
        return True

    # Check 2: see if a `hs` contains the cross point. Allow points on
    # boundaries, even for `Hp`.
    return Hpc(hs.p1, hs.p2).contains(x.point)


def _hs_contains_pt_strict(hs: Hs, pt: Pt) -> bool:
    """Numerical check. The strict one."""
    return Hp(hs.p1, hs.p2).contains(pt)


def _hs_contains_pt_with_epsilon(hs: Hs, pt: Pt) -> bool:
    """Numerical check. The loose one."""
    return Hpc(hs.p1, hs.p2).contains(pt)


def _esum_contains_pt_strict(esum: Esum, pt: Pt) -> bool:
    """Numerical check."""
    return any(
        all(_hs_contains_pt_strict(hs, pt) for hs in group) for group in esum.terms
    )


def _esum_contains_pt_with_epsilon(esum: Esum, pt: Pt) -> bool:
    """Numerical check."""
    return any(
        all(_hs_contains_pt_with_epsilon(hs, pt) for hs in group)
        for group in esum.terms
    )


def find_vertices(esum: Esum) -> t.Set[X]:
    crosses = find_all_xs([hs for term in esum.terms for hs in term])
    inside = list(
        mitt.unique_everseen(cross for cross in crosses if esum.contains_x(cross))
    )
    collapsed = collapse_xs(inside)
    return collapsed


def query_xs(xs: t.Iterable[X], poi: Pt, eps: float = 0.1) -> t.Iterable[X]:
    """Select cross points that are epsilon-close to the point-of-interest."""
    return [x for x in xs if x.point.distance(poi) < eps]


def query_x(crosses: t.Iterable[X], poi: Pt, eps: float = 0.1) -> X:
    """Find the first cross point that's epsilon-close to the point-of-interest."""
    results = query_xs(crosses, poi, eps)
    assert len(results) == 1
    return results[0]


@frozen_model
class XSegment(TodoMixin):
    x1: X
    x2: X
    debug_name: t.Optional[str] = debug_name_field

    def debug_info(self, names=False, length=True):
        suffix = ""

        if length:
            delta = self.x2.point.position - self.x1.point.position
            suffix += f" l={np.hypot(delta[0], delta[1])}"

        if names:
            return f"({self.x1.debug_name})-({self.x2.debug_name}){suffix}"
        else:
            x1_x = self.x1.point.x
            x1_y = self.x1.point.y
            x2_x = self.x2.point.x
            x2_y = self.x2.point.y

            return f"({x1_x}, {x1_y})-({x2_x}, {x2_y}){suffix}"


def hs_xs_index(xs: t.Iterable[X]) -> t.Dict[Hs, t.Set[X]]:
    """A cross point maps from a point to a pair of HSes. This maps from HSes
    to crosses.
    """
    index = {}
    for cross in xs:
        for hs in [cross.hs1, cross.hs2]:
            index.setdefault(hs, set()).add(cross)
    return index


@frozen_model
class GraphEdge(TodoMixin):
    node1: t.Any
    node2: t.Any
    meta: t.Any
    debug_name: t.Optional[str] = debug_name_field


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


def find_segments(xs: t.Iterable[X]) -> t.Sequence[XSegment]:
    cross_index = hs_xs_index(xs)

    all_segments = []
    for x_i, x_of_interest in enumerate(xs):
        for hs in x_of_interest.halfspaces:
            # 1. get neighbors for p1.hs1, p1.hs2
            # We need to retain order.
            xs_on_this_hs = list(cross_index[hs])
            if len(xs_on_this_hs) <= 1:
                continue

            segments = infer_smallest_segments(xs_on_this_hs, hs)
            all_segments.extend(segments)

    return list(mitt.unique_everseen(all_segments))


def infer_smallest_segments(xs: t.Sequence[X], hs: Hs) -> t.Sequence[XSegment]:
    """
    Args:
        xs: endpoints for segments. They all need to lie along a single `hs`.
            Need at least 2.
        hs: halfspace used to determine the sorting direction.
    Returns:
        Constructed segments. They should be as small as possible, there should
            be never an element of `xs` that's in the middle of an inferred
            segment.
    """
    # 1. Get a "stencil" vector from the halfspace points we're considering
    #     (AB). We need this vector to be non-zero. It will be true as long as
    #     the user defines a non-degenerate halfspace.
    # 2. Pick one of the halfspace's points as the coordinate origin (A).
    # 3. For each X, make a vector AX.
    # 4. Sort xs by the value of "AX . AB".
    # 5. Construct segments by a rolling window over sorted xs.

    # 1. Get stencil vector
    stencil_vec = hs.p2.position - hs.p1.position

    # 2. Coordinate origin
    coord_origin = hs.p1.position

    def _comparator(x: X):
        # 3. Get the AX vector
        ax_vec = x.point.position - coord_origin

        # 4. Sort by the dot product
        return np.dot(stencil_vec, ax_vec)

    xs_sorted = sorted(xs, key=_comparator)

    # 5. Connect subsequent pairs to get the smallest segments
    segments = [XSegment(x1, x2) for x1, x2 in mitt.windowed(xs_sorted, n=2)]
    return segments


def segment_on_boundary(esum: Esum, segment: XSegment) -> bool:
    pt1 = segment.x1.point
    pt2 = segment.x2.point
    mid_pt = Pt((pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2)

    e = _esum_contains_pt_with_epsilon(esum, mid_pt)
    s = _esum_contains_pt_strict(esum, mid_pt)

    return e and not s


def filter_segments(esum, segments):
    return [s for s in segments if segment_on_boundary(esum, s)]


def collapse_xs(xs: t.Iterable[X]) -> t.Sequence[X]:
    """Filters out bound crosses that correspond to the same halfspace pairs."""
    seen_set = set()
    seen_inverted_set = set()
    filtered = []
    for cross in xs:
        if cross in seen_set or cross in seen_inverted_set:
            continue

        seen_set.add(cross)
        seen_inverted_set.add(X(cross.hs2, cross.hs1))
        filtered.append(cross)

    return filtered


def named_esum(esum: Esum) -> Esum:
    """Traverse whole object graph and distribute unique debug names."""

    hs_names = {}
    pt_names = {}
    hs_counter = itertools.count()
    pt_counter = itertools.count()

    for term in esum.terms:
        for hs in term:
            if hs not in hs_names:
                hs_names[hs] = f"h_{next(hs_counter)}"

            for pt in [hs.p1, hs.p2]:
                if pt not in pt_names:
                    pt_names[pt] = f"p_{next(pt_counter)}"

    return Esum(
        SortedSet(
            frozenset(
                dataclasses.replace(
                    hs,
                    debug_name=hs_names[hs],
                    p1=dataclasses.replace(hs.p1, debug_name=pt_names[pt]),
                    p2=dataclasses.replace(hs.p2, debug_name=pt_names[pt]),
                )
                for hs in term
            )
            for term in esum.terms
        )
    )


def detect_segments(esum: Esum):
    """Run full algorithm."""
    vertices = find_vertices(esum=esum)
    segment_candidates = find_segments(vertices)
    boundary_segments = filter_segments(esum, segment_candidates)
    return boundary_segments
