from pathlib import Path

from .. import common_shapes, flat, io, plots


def _make_basic_shapes():
    triangle = common_shapes.triangle()
    rect = common_shapes.rect()
    return [
        triangle,
        rect,
        rect.difference(triangle)._replace(name="rect \\ triangle"),
        triangle.difference(rect)._replace(name="triagle \\ rect"),
        rect.union(triangle)._replace(name="rect | triangle"),
        rect.intersection(triangle)._replace(name="rect ^ triangle"),
    ]


RESULTS_PATH = Path("./data")


def _plot(esum, vertices, path, name):
    fig, ax = plots.subplots(1, 1)

    xlim = [0, 20]
    ylim = [0, 20]
    plots.plot_esum_boundaries(esum, ax=ax, xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=ax, xlim=xlim, ylim=ylim)
    ax.set_title(name)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True)

    for shape_i, (esum, name) in enumerate(
        [*_make_basic_shapes(), common_shapes.letter_c()]
    ):
        vertices = flat.find_vertices(esum=esum)

        with open(RESULTS_PATH / f"shape_{shape_i}.json", "w") as f:
            io.dump_shape(esum=esum, vertices=vertices, f=f)

        _plot(esum, vertices, RESULTS_PATH / f"shape_{shape_i}.png", name)


if __name__ == "__main__":
    main()
