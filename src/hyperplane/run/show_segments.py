from pathlib import Path

from .. import common_shapes, flat, plots, shape_gen

RESULTS_PATH = Path("./data/segments")


def _plot(esum, vertices, segments, path, name):
    fig, axes = plots.subplots(1, 2)

    xlim = [0, 20]
    ylim = [0, 20]

    plots.plot_esum_boundaries(esum, ax=axes[0], xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=axes[0], xlim=xlim, ylim=ylim)
    axes[0].set_title(name)

    plots.draw_segments(axes[1], segments, xlim, ylim)

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
        vertices = flat.find_vertices(esum=esum)
        segments = flat.segments(vertices)
        boundary_segments = flat.filter_segments(esum, segments)

        _plot(
            esum=esum,
            vertices=vertices,
            segments=boundary_segments,
            path=RESULTS_PATH / f"shape_{shape_i}.png",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
