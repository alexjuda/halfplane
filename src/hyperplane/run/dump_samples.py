from pathlib import Path

from ..flat import Esum, Pt, Hp, Hpc
from .. import flat
from .. import io
from .. import plots


def _make_c():
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

    return external.difference(internal)


def _make_basic_shapes():
    triangle = Esum(
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
        }
    )

    rect = Esum(
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
        }
    )
    return [
        triangle,
        rect,
        rect.difference(triangle),
        triangle.difference(rect),
        rect.union(triangle),
        rect.intersection(triangle),
    ]


RESULTS_PATH = Path("./data")


def _plot(esum, vertices, path):
    fig, ax = plots.subplots(1, 1)

    xlim = [0, 20]
    ylim = [0, 20]
    plots.plot_esum_boundaries(esum, ax=ax, xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=ax, xlim=xlim, ylim=ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True)

    for shape_i, shape in enumerate([*_make_basic_shapes(), _make_c()]):
        vertices = flat.find_vertices(esum=shape)

        with open(RESULTS_PATH / f"shape_{shape_i}.json", "w") as f:
            io.dump_shape(esum=shape, vertices=vertices, f=f)

        _plot(shape, vertices, RESULTS_PATH / f"shape_{shape_i}.png")


if __name__ == "__main__":
    main()
