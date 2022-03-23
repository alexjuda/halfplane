import dataclasses
from pathlib import Path

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/groups")


def _plot(esum, path, name):
    n_groups = len(esum.terms)
    fig, axes = plots.subplots(n_groups, 2)

    xlim = [0, 20]
    ylim = [0, 20]

    for group_i, (group, ax_row) in enumerate(zip(esum.terms, axes)):
        group_esum = dataclasses.replace(esum, terms={group})
        plots.plot_esum_boundaries(group_esum, ax=ax_row[0], xlim=xlim, ylim=ylim)

        vertices = flat.find_vertices(group_esum)
        plots.draw_vertices(vertices, ax=ax_row[0], xlim=xlim, ylim=ylim)
        ax_row[0].set_title(f"group {group_i}")

        segments = flat.segments(vertices)
        plots.draw_segments(ax_row[1], segments, xlim, ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.letter_c()]):
        _plot(
            esum=esum,
            path=RESULTS_PATH / f"shape_{shape_i}.png",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
