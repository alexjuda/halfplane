from pathlib import Path

import matplotlib.pyplot as plt

from ..flat import Esum, Pt, Hp, Hpc
from .. import flat
from .. import io
from .. import plots


def _make_shapes():
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

    square = Esum(
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
        square,
        square.difference(triangle),
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

    for shape_i, shape in enumerate(_make_shapes()):
        vertices = flat.find_vertices(esum=shape)

        with open(RESULTS_PATH / f"shape_{shape_i}.json", "w") as f:
            io.dump_shape(esum=shape, vertices=vertices, f=f)

        _plot(shape, vertices, RESULTS_PATH / f"shape_{shape_i}.png")


if __name__ == "__main__":
    main()
