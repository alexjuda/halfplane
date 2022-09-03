from pathlib import Path

from .. import common_shapes, plots, shape_gen

RESULTS_PATH = Path("./data/esums")


def _plot(esum, path, name):
    fig, axes = plots.subplots(1, 1)

    xlim = ylim = [-2, 14]

    plots.plot_esum_boundaries(esum, ax=axes, xlim=xlim, ylim=ylim)

    # TODO: vertices if we want
    # vertices = flat.find_vertices(group_esum)
    # plots.draw_vertices(vertices, ax=ax_row[0], xlim=xlim, ylim=ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate(
        [
            common_shapes.letter_c(),
            shape_gen.rect_chain(n=4, stride_x=3, stride_y=3),
            shape_gen.rect_chain(n=10, stride_x=3, stride_y=3),
        ]
    ):
        esum_name = f"_{esum.debug_name}" if esum.debug_name else ""
        _plot(
            esum=esum,
            path=RESULTS_PATH / f"shape_{shape_i}{esum_name}.png",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
