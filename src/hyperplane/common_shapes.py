from .flat import Esum, Pt, Hp, Hpc


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

    return external.difference(internal)._replace(name="letter C")


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
