from pathlib import Path

import matplotlib.pyplot as plt

from .. import common_shapes, plots

RESULTS_PATH = Path("./data/slides")


def _plot(esum, path, name):
    fig, axes = plots.subplots(1, 1)

    xlim = ylim = [-1, 16]

    plots.plot_esum_boundaries(esum, ax=axes, xlim=xlim, ylim=ylim)

    axes.xaxis.set_major_locator(plt.NullLocator())
    axes.yaxis.set_major_locator(plt.NullLocator())

    for spine in ["top", "right", "bottom", "left"]:
        axes.spines[spine].set_visible(False)

    axes.get_legend().remove()

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate(
        [
            common_shapes.triangle(),
            common_shapes.letter_c(),
            common_shapes.letter_c_external(),
            common_shapes.letter_c_internal(),
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
