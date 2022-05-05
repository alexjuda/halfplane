import dataclasses
from . import flat


def rect(min_x: float, min_y: float, width: float, height: float) -> flat.Esum:
    #
    #   p1  h1    p2
    #    ┼───┬───┼
    #    │   ▼   │
    # h4 ├►     ◄┤ h2
    #    │   ▲   │
    #    ┼───┴───┼
    #   p4  h3    p3
    #
    p1 = flat.Pt(min_x, min_y + height, debug_name="p1")
    p2 = flat.Pt(min_x + width, min_y + height, debug_name="p1")
    p3 = flat.Pt(min_x + width, min_y, debug_name="p3")
    p4 = flat.Pt(min_x, min_y, debug_name="p4")

    return flat.Esum(
        {
            frozenset(
                [
                    flat.Hpc(p2, p1, debug_name="h1"),
                    flat.Hpc(p3, p2, debug_name="h2"),
                    flat.Hpc(p4, p3, debug_name="h3"),
                    flat.Hpc(p1, p4, debug_name="h4"),
                ]
            )
        },
        debug_name="rect",
    )


def _update(dc, **prop_fns):
    current_vals = {prop: getattr(dc, prop) for prop in prop_fns.keys()}

    return dataclasses.replace(
        dc,
        **{prop: fn(current_vals[prop]) for prop, fn in prop_fns.items()},
    )


def rect_chain(
    n: int,
    start_x: float = 0.0,
    start_y: float = 0.0,
    width: float = 4.0,
    height: float = 4.0,
    stride_x: float = 1.0,
    stride_y: float = 1.0,
) -> flat.Esum:
    rects = []

    for rect_i in range(n):
        a_rect = rect(
            min_x=start_x + rect_i * stride_x,
            min_y=start_y + rect_i * stride_y,
            width=width,
            height=height,
        )
        rects.append(a_rect)

    first_rect, *rest_rects = rects
    union = first_rect
    for a_rect in rest_rects:
        union = union.union(a_rect)

    return dataclasses.replace(union, debug_name="rect_chain")
