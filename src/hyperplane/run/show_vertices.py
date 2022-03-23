import typing as t
from pathlib import Path

import matplotlib.patches

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/vertices")


def _draw_labelled_vertices(ax, vertices: t.Sequence[flat.BoundsCross], xlim, ylim):
    for vertex_i, vertex in enumerate(vertices):
        pt = vertex.point
        patch = matplotlib.patches.Circle(pt, radius=0.1)
        ax.add_patch(patch)
        ax.text(*pt, str(vertex_i))

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")


def _plot(esum, vertices, path, name):
    fig, axes = plots.subplots(1, 2)

    xlim = [0, 20]
    ylim = [0, 20]

    plots.plot_esum_boundaries(esum, ax=axes[0], xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=axes[0], xlim=xlim, ylim=ylim)
    axes[0].set_title(name)

    _draw_labelled_vertices(axes[1], vertices, xlim=xlim, ylim=ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.letter_c()]):
        vertices = flat.find_vertices(esum=esum)
        segments = flat.segments(vertices)

        _plot(
            esum=esum,
            vertices=list(vertices),
            path=RESULTS_PATH / f"shape_{shape_i}.png",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
