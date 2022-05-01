import dataclasses

from .flat import Esum, Hp, Hpc, Pt


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
    external = Esum(
        {
            frozenset(
                [
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
                ]
            )
        }
    )

    internal = Esum(
        {
            frozenset(
                [
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
                ]
            )
        }
    )

    return dataclasses.replace(external.difference(internal), name="letter C")


def triangle():
    return Esum(
        {
            frozenset(
                [
                    # diagonal line (/)
                    Hpc(
                        Pt(8, 10),
                        Pt(4, 2),
                    ),
                    # diagonal line (\)
                    Hp(
                        Pt(12, 2),
                        Pt(10, 10),
                    ),
                    # horizontal line (-)
                    Hpc(
                        Pt(2, 2),
                        Pt(8, 2),
                    ),
                ]
            )
        },
        name="triangle",
    )


def rect():
    return Esum(
        {
            frozenset(
                [
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
                ]
            )
        },
        name="rect",
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

    part1 = Esum(
        {
            frozenset(
                [
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
                ]
            )
        },
    )

    part2 = Esum(
        {
            frozenset(
                [
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
                ]
            )
        },
    )

    part3 = Esum(
        {
            frozenset(
                [
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
                ]
            )
        },
    )

    return part1.union(part2).union(part3)
