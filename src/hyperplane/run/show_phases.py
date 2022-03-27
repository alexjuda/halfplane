import typing as t
from pathlib import Path

import matplotlib.patches

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/phases")


def _plot(esum, path, name):
    fig, axes = plots.subplots(1, 2)

    xlim = ylim = [-2, 14]

    plots.plot_esum_boundaries(esum, ax=axes[0], xlim=xlim, ylim=ylim)

    vertices = flat.find_vertices(esum)
    index = flat.hs_crosses_index(vertices)
    p1 = flat.query_cross(vertices, flat.Pt(10, 9))
    # TODO: get neighbors for p1.hs1, p1.hs2
    # TODO: order by HS direction
    # TODO: connect subsequent pairs to get the smallest segments
    # TODO: classify segments
    breakpoint()
    plots.draw_vertices(vertices, ax=axes[1], xlim=xlim, ylim=ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.crude_c()]):
        _plot(
            esum=esum,
            path=RESULTS_PATH / f"shape_{shape_i}.png",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
