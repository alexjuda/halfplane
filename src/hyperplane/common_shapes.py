import dataclasses

from .flat import Esum, Eterm, Hpc, Pt, Hs


def letter_c_external():
    return Esum.from_terms(
        Eterm.from_hses(
            # vertical line (|)
            Hpc(
                Pt(2, 10),
                Pt(2, 0),
            ),
            # diagonal line (/)
            Hpc(
                Pt(6, 14),
                Pt(2, 10),
            ),
            # horizontal line (-)
            Hpc(
                Pt(10, 14),
                Pt(6, 14),
            ),
            # vertical line (|)
            Hpc(
                Pt(12, 10),
                Pt(12, 14),
            ),
            # diagonal line (\)
            Hpc(
                Pt(2, 6),
                Pt(6, 2),
            ),
            # horizontal line (-)
            Hpc(
                Pt(6, 2),
                Pt(10, 2),
            ),
        ),
    )


def letter_c_internal():
    return Esum.from_terms(
        Eterm.from_hses(
            # vertical line (|)
            Hpc(
                Pt(4, 10),
                Pt(4, 0),
            ),
            # diagonal line (/)
            Hpc(
                Pt(8, 14),
                Pt(4, 10),
            ),
            # horizontal line (-)
            Hpc(
                Pt(10, 12),
                Pt(6, 12),
            ),
            # diagonal line (\)
            Hpc(
                Pt(4, 6),
                Pt(8, 2),
            ),
            # horizontal line (-)
            Hpc(
                Pt(6, 4),
                Pt(10, 4),
            ),
        )
    )


def letter_c():
    # letter C:
    #
    #      -------
    #     /      |
    #    /   -----
    #   /   /
    #   |  /
    #   |  |
    #   |  \
    #   \   \
    #    \   -----
    #     \      |
    #      -------

    return dataclasses.replace(
        letter_c_external().difference(letter_c_internal()),
        name="letter C",
    )


def letter_chi():
    """Originally devised as a subset of letter C that was problematic for
    segment detection. Later it turned out that it wasn't easy to reproduce the error."""

    vertical = Esum.from_terms(
        Eterm.from_hses(
            # horizontal line (-)
            Hpc(
                Pt(10, 13),
                Pt(6, 13),
            ),
            # vertical line (|)
            Hpc(
                Pt(2, 10),
                Pt(2, 0),
            ),
            # vertical line (|)
            Hpc(
                Pt(4, 0),
                Pt(4, 10),
            ),
            # horizontal line (-)
            Hpc(
                Pt(6, -1),
                Pt(10, -1),
            ),
        ),
    )

    bottom = Esum.from_terms(
        Eterm.from_hses(
            # vertical line (|)
            Hpc(
                Pt(-1, 10),
                Pt(-1, 0),
            ),
            # diagonal line (\)
            Hpc(
                Pt(8, 2),
                Pt(4, 6),
            ),
            # diagonal line (\)
            Hpc(
                Pt(2, 6),
                Pt(6, 2),
            ),
            # horizontal line (-)
            Hpc(
                Pt(6, 2),
                Pt(10, 2),
            ),
        ),
    )

    esum = vertical.union(bottom)

    return dataclasses.replace(esum, name="letter Chi")


def triangle():
    return Esum.from_terms(
        Eterm.from_hses(
            # diagonal line (/)
            Hpc(
                Pt(8, 10),
                Pt(3, 1),
                debug_name="/",
            ),
            # diagonal line (\)
            Hpc(
                Pt(9, 1),
                Pt(4, 10),
                debug_name="\\",
            ),
            # horizontal line (-)
            Hpc(
                Pt(2, 2),
                Pt(10, 2),
                debug_name="-",
            ),
        ),
        debug_name="triangle",
    )


def rect():
    return Esum.from_terms(
        Eterm.from_hses(
            # vertical line (|)
            Hpc(
                Pt(3, 5),
                Pt(3, -1),
            ),
            # vertical line (|)
            Hpc(
                Pt(15, 1),
                Pt(15, 6),
            ),
            # horizontal line (-)
            Hpc(
                Pt(1, 10),
                Pt(10, 10),
            ),
            # horizontal line (-)
            Hpc(
                Pt(11, 17),
                Pt(1, 17),
            ),
        ),
        debug_name="rect",
    )


def crude_c():
    # The C-like shape in-between:
    #
    # ─┼─┼───────────┼
    # ─┼─┼───────────┼
    #  │ │           │
    #  │ │           │
    #  │ │           │
    # ─┼─┼───────────┼
    # ─┼─┼───────────┼
    #
    # It's a union of three parts.
    #
    # part 1:
    # ───────────────┼
    # ───────────────┼
    #
    # part 2:
    #  │ │
    #  │ │
    #  │ │
    #  │ │
    #  │ │
    #  │ │
    #  │ │
    #
    # part 3:
    # ───────────────┼
    # ───────────────┼

    part1 = Esum.from_terms(
        Eterm.from_hses(
            # ---- vertical lines ----
            # right-most vertical line (|)
            Hpc(
                Pt(10, 0),
                Pt(10, 11),
            ),
            # ---- horizontal lines ----
            # top-most horizontal line (-)
            Hpc(
                Pt(0, 9),
                Pt(11, 9),
            ),
            # horizontal line (-)
            Hpc(
                Pt(12, 10),
                Pt(-1, 10),
            ),
        )
    )

    part2 = Esum.from_terms(
        Eterm.from_hses(
            # ---- vertical lines ----
            # 1st, left-most vertical line (|)
            Hpc(
                Pt(1, 11),
                Pt(1, 0),
            ),
            # 2nd vertical line (|)
            Hpc(
                Pt(2, -1),
                Pt(2, 12),
            ),
        )
    )

    part3 = Esum.from_terms(
        Eterm.from_hses(
            # ---- vertical lines ----
            # right-most vertical line (|)
            Hpc(
                Pt(10, 0),
                Pt(10, 11),
            ),
            # ---- horizontal lines ----
            # bottom-most horizontal line (-)
            Hpc(
                Pt(0, 1),
                Pt(11, 1),
            ),
            # horizontal line (-)
            Hpc(
                Pt(12, 2),
                Pt(-1, 2),
            ),
        )
    )

    return part1.union(part2).union(part3)


def _vertical_hpc_facing_right(x: float) -> Hpc:
    return Hpc(p1=Pt(x=x, y=10), p2=Pt(x=x, y=0))


def _horizontal_hpc_facing_up(y: float) -> Hpc:
    return Hpc(p1=Pt(x=0, y=y), p2=Pt(x=10, y=y))


def _flip_hs(hs: Hs) -> Hs:
    """
    Flip the order without changing the strictness.
    """
    return type(hs)(p1=hs.p2, p2=hs.p1)


def big_l() -> Esum:
    vertical = Esum.from_terms(
        Eterm.from_hses(
            _vertical_hpc_facing_right(x=2),
            _flip_hs(_vertical_hpc_facing_right(x=3)),
        ),
    )
    horizontal = Esum.from_terms(
        Eterm.from_hses(
            _horizontal_hpc_facing_up(y=2),
            _flip_hs(_horizontal_hpc_facing_up(y=3)),
        )
    )
    bound = Esum.from_terms(
        Eterm.from_hses(
            _horizontal_hpc_facing_up(y=1),
            _flip_hs(_horizontal_hpc_facing_up(y=10)),
            _vertical_hpc_facing_right(x=1),
            _flip_hs(_vertical_hpc_facing_right(x=10)),
        )
    )
    return vertical.union(horizontal).intersection(bound)
