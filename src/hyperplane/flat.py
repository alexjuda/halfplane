import dataclasses
import itertools
import math
import typing as t
from numbers import Number

import more_itertools as mitt
import numpy as np

from .core import Coord
from .generic_structs import FOSet

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


# A sentinel to note that a lazy property hasn't been calculated yet.
# Allows returning `None` as a valid property value.
EMPTY_PROP = object()


def lazy_prop(method):
    def _inner(self):
        prop_name = method.__name__
        attr_name = f"_{prop_name}"

        if getattr(self, attr_name) == EMPTY_PROP:
            val = method(self)
            object.__setattr__(self, attr_name, val)

        return getattr(self, attr_name)

    return _inner


class TodoMixin:
    pass


@frozen_model
class Pt(TodoMixin):
    x: Coord
    y: Coord
    debug_name: t.Optional[str] = debug_name_field

    @property
    def position2d(self) -> np.ndarray:
        """2d position vector."""
        return np.array([self.x, self.y])

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
    a1 = half_space.p2.x - half_space.p1.x
    a2 = half_space.p2.y - half_space.p1.y
    b1 = point.x - half_space.p1.x
    b2 = point.y - half_space.p1.y

    return a1 * b2 - a2 * b1


def _line_params(p1: Pt, p2: Pt) -> t.Optional[t.Tuple[Number, Number]]:
    dy = p2.y - p1.y
    dx = p2.x - p1.x

    try:
        a = float(dy) / float(dx)
    except ZeroDivisionError:
        return None

    b = p1.y - a * p1.x

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


def _intersection_point2(hs1: Hs, hs2: Hs) -> t.Optional[Pt]:
    """Reimplementation of `_intersection_point2()`.
    Turns out it's 2-3 times slower than the original one, so probably we won't
    be using it.
    """
    a1 = [hs1.p1.x, hs1.p1.y]
    a2 = [hs1.p2.x, hs1.p2.y]

    b1 = [hs2.p1.x, hs2.p1.y]
    b2 = [hs2.p2.x, hs2.p2.y]

    intersection = _get_intersect(a1, a2, b1, b2)
    if intersection is not None:
        return Pt(x=intersection[0], y=intersection[1])
    else:
        return None


# Taken from https://stackoverflow.com/a/42727584
# Author: Norbu Tsering
def _get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return None
        # return (float("inf"), float("inf"))
    return (x / z, y / z)


# def _bbox_from_


@frozen_model
class X(TodoMixin):
    """Cross point between two halspaces. Doesn't calculate coordinates until
    `point` is called.
    """

    hs1: Hs
    hs2: Hs
    debug_name: t.Optional[str] = debug_name_field

    _point: t.Optional[Pt] = dataclasses.field(
        init=False,
        repr=False,
        hash=False,
        compare=False,
        default=EMPTY_PROP,
    )

    @property
    @lazy_prop
    def point(self) -> Pt:
        return _intersection_point(self.hs1, self.hs2)

    @property
    def halfspaces(self) -> t.Sequence[Hs]:
        return [self.hs1, self.hs2]


@frozen_model
class Box:
    min_x: Coord
    min_y: Coord
    max_x: Coord
    max_y: Coord


def box_contains_pt(box: Box, pt: Pt, epsilon: float = 0.01):
    return (
        box.min_x - epsilon < pt.x < box.max_x + epsilon
        and box.min_y - epsilon < pt.y < box.max_y + epsilon
    )


@frozen_model
class Eterm:
    """
    A group of halfspaces joined with the "and" operation.
    """

    hses: FOSet[Hs]

    @classmethod
    def from_hses(cls, *args: Hs):
        return cls(hses=FOSet(args))

    @property
    def xs(self) -> t.FrozenSet[X]:
        xs = find_all_xs(self.hses)
        if len(xs) == 0:
            raise ValueError(f"No crosses for eterm {self}")

        return xs

    @property
    def bbox(self) -> Box:
        return points_bbox(map(lambda x: x.point, self.xs))


def points_bbox(pts: t.Iterable[Pt]) -> Box:
    # 1. Get all hs crosses
    # 2. Get all points
    # 3. Find min and max by dimension
    min_x = None
    min_y = None
    max_x = None
    max_y = None

    for pt in pts:
        # min
        if min_x is None or pt.x < min_x:
            min_x = pt.x
        if min_y is None or pt.y < min_y:
            min_y = pt.y

        # max
        if max_x is None or max_x < pt.x:
            max_x = pt.x
        if max_y is None or max_y < pt.y:
            max_y = pt.y

    return Box(
        min_x=min_x,
        min_y=min_y,
        max_x=max_x,
        max_y=max_y,
    )


@frozen_model
class Esum(TodoMixin):
    """Expression sum. Basic shape representation.

    Uses two-level sets of halfspaces. The outer set is considered a union of
    terms. The inner set (AKA a term) is considered an intersection of
    halfspaces.
    """

    eterms: FOSet[Eterm]
    "Each term is a group of intersecting halfspaces."

    name: t.Optional[str] = None
    debug_name: t.Optional[str] = debug_name_field

    @classmethod
    def from_terms(cls, *args: Eterm, debug_name: t.Optional[str] = None):
        return cls(eterms=FOSet(args), debug_name=debug_name)

    @classmethod
    @property
    def empty(cls):
        return cls.from_terms()

    def union(self, other: "Esum") -> "Esum":
        return Esum(self.eterms | other.eterms)

    def intersection(self, other: "Esum") -> "Esum":
        new_terms = []
        for self_term in self.eterms:
            for other_term in other.eterms:
                new_hses = self_term.hses ^ other_term.hses
                new_terms.append(Eterm(new_hses))

        return Esum(FOSet(new_terms))

    def difference(self, other: "Esum") -> "Esum":
        return self.intersection(other.conjugate)

    def contains(self, point: Pt) -> bool:
        return _esum_contains_pt_strict(self, point)

    @property
    def conjugate(self) -> "Esum":
        # I think the general pattern is like this:
        # 1. Start with Esum
        # 2. Generate Carthesian product of items in terms. Each generated
        #     tuple will be a term in the output Esum.
        # 3. Negate each item in each term.
        conjugate_terms = []
        for product_term in itertools.product(
            *map(lambda term: term.hses, self.eterms)
        ):
            conjugate_group = []
            for hs in product_term:
                conjugate_group.append(hs.conjugate)

            # Avoid empty inner sets
            if len(conjugate_group) > 0:
                conjugate_terms.append(Eterm(hses=FOSet(conjugate_group)))

        return Esum(eterms=FOSet(conjugate_terms))

    # def contains_x(self, x: "X") -> bool:
    #     """Checks if cross point `x` is a member of this Esum. This includes
    #     crosspoints lying on the boundary, regardless of Hp/Hpc strictness.
    #     """
    #     # TODO: should the inner `all` be switched to an any?
    #     return any(
    #         all(_hs_contains_x(hs, x) for hs in term.hses) for term in self.eterms
    #     )


def find_all_xs(hses: t.Iterable[Hs]) -> t.Set[X]:
    return {
        x
        for hs1, hs2 in itertools.combinations(hses, 2)
        if (x := X(hs1, hs2)).point is not None
    }


# ----- esum-pt ------


def _esum_contains_pt_strict(esum: Esum, pt: Pt) -> bool:
    """Numerical check."""
    return any(
        all(_hs_contains_pt_strict(hs, pt) for hs in term.hses) for term in esum.eterms
    )


def _esum_contains_pt_with_eps(esum: Esum, pt: Pt) -> bool:
    """Numerical check."""
    return any(
        all(_hs_contains_pt_with_eps(hs, pt) for hs in term.hses)
        for term in esum.eterms
    )


# ----- esum-seg ------


def _esum_contains_seg_with_eps(esum: Esum, segment: "XSegment") -> bool:
    # The lazy check should work with both HPs and HPCs
    common_hp = Hp(p1=segment.common_hs.p1, p2=segment.common_hs.p2)
    common_hpc = Hpc(common_hp.p1, common_hp.p2)

    p1 = segment.x1.point
    p2 = segment.x2.point
    mid_pt = Pt(
        x=(p1.x + p2.x) / 2,
        y=(p1.y + p2.y) / 2,
    )

    for eterm in esum.eterms:
        # lazy check
        if common_hp in eterm.hses or common_hpc in eterm.hses:
            # This assumes that each term is a convex polygon.
            # TODO: should we also check the segment endpoints?
            return True

        # numerical check
        if _eterm_contains_pt_with_eps(eterm, mid_pt):
            return True

    return False


def _esum_contains_seg_strict(esum: Esum, segment: "XSegment") -> bool:
    # The lazy check should work with both HPs and HPCs
    common_hp = Hp(p1=segment.common_hs.p1, p2=segment.common_hs.p2)
    common_hpc = Hpc(common_hp.p1, common_hp.p2)

    p1 = segment.x1.point
    p2 = segment.x2.point
    mid_pt = Pt(
        x=(p1.x + p2.x) / 2,
        y=(p1.y + p2.y) / 2,
    )

    for eterm in esum.eterms:
        # lazy check
        if common_hp in eterm.hses or common_hpc in eterm.hses:
            # This assumes that each term is a convex polygon.
            # TODO: should we also check the segment endpoints?
            return False


        # numerical check
        if _eterm_contains_pt_strict(eterm, mid_pt):
            return True

    return False


# ----- eterm-pt ------


def _eterm_contains_pt_with_eps(eterm: Eterm, pt: Pt) -> bool:
    """Numerical check."""
    return all(_hs_contains_pt_with_eps(hs, pt) for hs in eterm.hses)


def _eterm_contains_pt_strict(eterm: Eterm, pt: Pt) -> bool:
    """Numerical check."""
    return all(_hs_contains_pt_strict(hs, pt) for hs in eterm.hses)


# ----- esum-x ------


def _esum_contains_x_with_eps(esum: Esum, x: X):
    return any(
        all(_hs_contains_x_with_eps(hs, x) for hs in eterm.hses)
        for eterm in esum.eterms
    )


# ----- hs-x ------


def _hs_contains_x_with_eps(hs: Hs, x: X):
    # Check 1: see if `hs` was used to create this `cross`. This should
    # alleviate numerical errors.
    if hs in {x.hs1, x.hs2}:
        return True

    # Check 2: see if a `hs` contains the cross point. Allow points on
    # boundaries, even for `Hp`.
    return _hs_contains_pt_with_eps(hs, x.point)


# ----- hs-pt ------


def _hs_contains_pt_strict(hs: Hs, pt: Pt) -> bool:
    """Numerical check. The strict one."""
    return Hp(hs.p1, hs.p2).contains(pt)


def _hs_contains_pt_with_eps(hs: Hs, pt: Pt) -> bool:
    """Numerical check. The loose one."""
    return Hpc(hs.p1, hs.p2).contains(pt)


def find_vertices(esum: Esum) -> t.Set[X]:
    crosses = find_all_xs([hs for term in esum.eterms for hs in term.hses])
    # inside = list(
    #     mitt.unique_everseen(cross for cross in crosses if esum.contains_x(cross))
    # )
    inside = filter(lambda x: _esum_contains_x_with_eps(esum, x), crosses)
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
    hs1: Hs
    common_hs: Hs
    hs3: Hs
    debug_name: t.Optional[str] = debug_name_field

    @classmethod
    def from_xs(cls, x1: X, x2: X) -> "XSegment":
        x1_hses = set(x1.halfspaces)
        x2_hses = set(x2.halfspaces)
        common_hses = x1_hses & x2_hses
        assert len(common_hses) == 1, (
            "A segment should be formed by exactly 1 common HS. We've "
            f"got {len(common_hses)}: {common_hses}"
        )
        (hs1,) = x1_hses.difference(common_hses)
        (common_hs,) = common_hses
        (hs3,) = x2_hses.difference(common_hses)

        return XSegment(hs1, common_hs, hs3)

    @property
    def x1(self) -> X:
        return X(self.hs1, self.common_hs)

    @property
    def x2(self) -> X:
        return X(self.common_hs, self.hs3)

    def debug_info(self, names=False, length=True):
        suffix = ""

        if length:
            delta = self.x2.point.position2d - self.x1.point.position2d
            suffix += f" l={np.hypot(delta[0], delta[1])}"

        if names:
            return f"({self.x1.debug_name})-({self.x2.debug_name}){suffix}"
        else:
            x1_x = self.x1.point.x
            x1_y = self.x1.point.y
            x2_x = self.x2.point.x
            x2_y = self.x2.point.y

            return f"({x1_x}, {x1_y})-({x2_x}, {x2_y}){suffix}"

    def __str__(self):
        return f"<XSegment {self.debug_info(names=False, length=False)}>"


def hs_xs_index(xs: t.Iterable[X]) -> t.Dict[Hs, t.Set[X]]:
    """A cross point maps from a point to a pair of HSes. This maps from HSes
    to crosses.
    """
    index = {}
    for cross in xs:
        for hs in [cross.hs1, cross.hs2]:
            index.setdefault(hs, set()).add(cross)
    return index


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
    stencil_vec = hs.p2.position2d - hs.p1.position2d

    # 2. Coordinate origin
    coord_origin = hs.p1.position2d

    def _comparator(x: X):
        # 3. Get the AX vector
        ax_vec = x.point.position2d - coord_origin

        # 4. Sort by the dot product
        return np.dot(stencil_vec, ax_vec)

    xs_sorted = sorted(xs, key=_comparator)

    # 5. Connect subsequent pairs to get the smallest segments
    segments = [XSegment.from_xs(x1, x2) for x1, x2 in mitt.windowed(xs_sorted, n=2)]
    return segments


def segment_on_boundary(esum: Esum, segment: XSegment) -> bool:
    # FIXME
    # pt1 = segment.x1.point
    # pt2 = segment.x2.point
    # mid_pt = Pt((pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2)

    # e = _esum_contains_pt_with_epsilon(esum, mid_pt)
    # s = _esum_contains_pt_strict(esum, mid_pt)

    e = _esum_contains_seg_with_eps(esum, segment)
    s = _esum_contains_seg_strict(esum, segment)

    return e and not s


def filter_segments(esum, segments):
    return [s for s in segments if segment_on_boundary(esum, s)]


def collapse_xs(xs: t.Iterable[X]) -> t.Sequence[X]:
    """Filters out xs that correspond to the same halfspace pairs."""
    seen_set = set()
    seen_inverted_set = set()
    filtered = []
    for x in xs:
        if x in seen_set or x in seen_inverted_set:
            continue

        seen_set.add(x)
        seen_inverted_set.add(X(x.hs2, x.hs1))
        filtered.append(x)

    return filtered


def named_esum(esum: Esum) -> Esum:
    """Traverse whole object graph and distribute unique debug names."""

    hs_names = {}
    pt_names = {}
    hs_counter = itertools.count()
    pt_counter = itertools.count()

    for term in esum.eterms:
        for hs in term.hses:
            if hs not in hs_names:
                hs_names[hs] = f"h_{next(hs_counter)}"

            for pt in [hs.p1, hs.p2]:
                if pt not in pt_names:
                    pt_names[pt] = f"p_{next(pt_counter)}"

    return Esum(
        eterms=FOSet(
            [
                Eterm.from_hses(
                    *[
                        dataclasses.replace(
                            hs,
                            debug_name=hs_names[hs],
                            p1=dataclasses.replace(hs.p1, debug_name=pt_names[pt]),
                            p2=dataclasses.replace(hs.p2, debug_name=pt_names[pt]),
                        )
                        for hs in term.hses
                    ]
                )
                for term in esum.eterms
            ]
        ),
        debug_name=esum.debug_name,
    )


def detect_boundary(esum: Esum):
    """Run full algorithm."""
    vertices = find_vertices(esum=esum)
    segment_candidates = find_segments(vertices)
    boundary_segments = filter_segments(esum, segment_candidates)
    return boundary_segments
