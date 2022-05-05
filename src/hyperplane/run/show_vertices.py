import typing as t
from pathlib import Path

import matplotlib.patches

from .. import common_shapes, flat, plots

RESULTS_PATH = Path("./data/vertices")


def _draw_labelled_vertices(ax, vertices: t.Sequence[flat.BoundsCross], glossary, xlim, ylim):
    for vertex in vertices:
        pt = vertex.point
        patch = matplotlib.patches.Circle((pt.x, pt.y), radius=0.1)
        ax.add_patch(patch)
        ax.text(pt.x, pt.y, s=glossary.name(vertex))

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")


def _plot(esum, vertices, vertex_glossary, path, name):
    fig, axes = plots.subplots(1, 2)

    xlim = [0, 20]
    ylim = [0, 20]

    plots.plot_esum_boundaries(esum, ax=axes[0], xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=axes[0], xlim=xlim, ylim=ylim)
    axes[0].set_title(name)

    _draw_labelled_vertices(axes[1], vertices, vertex_glossary, xlim=xlim, ylim=ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.letter_c()]):
        vertices = flat.find_vertices(esum=esum)
        # segments = flat.segments(vertices)
        vertex_gls = flat.Glossary(vertices, "v")
        # seg_gls = flat.Glossary(segments, "segment")

        _plot(
            esum=esum,
            vertices=vertices,
            vertex_glossary=vertex_gls,
            path=RESULTS_PATH / f"shape_{shape_i}.png",
            name=esum.name,
        )

        vertex_names = [vertex_gls.name(v) for v in vertices]
        print()


if __name__ == "__main__":
    main()
