import dataclasses
from pathlib import Path

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/esums")


def _plot(esum, path, name):
    fig, axes = plots.subplots(1, 1)

    xlim = [0, 20]
    ylim = [0, 20]

    plots.plot_esum_boundaries(esum, ax=axes, xlim=xlim, ylim=ylim)

    # TODO: vertices if we want
    # vertices = flat.find_vertices(group_esum)
    # plots.draw_vertices(vertices, ax=ax_row[0], xlim=xlim, ylim=ylim)

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
