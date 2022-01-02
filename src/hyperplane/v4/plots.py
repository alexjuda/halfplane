import functools
import math
import typing as t
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

from .flat import Hp, Hpc, Pt, Hs, Esum


def _datapoints(esum: Esum, x_iter, y_iter) -> np.ndarray:
    """Returns [X*Y x 3] array of data point rows, where:
    - col 0: x coordinate
    - col 1: y coordinate
    - col 2: inside esum or not (bool)
    """
    return np.array([[x, y, esum.contains(Pt(x, y))] for x in x_iter for y in y_iter])


@functools.singledispatch
def _plot_hs(hs, ax: plt.Axes, xlim, ylim):
    raise NotImplementedError()


def _rotate_vector(x: float, y: float, degrees) -> t.Tuple[float, float]:
    # Rotation matrix is:
    # [[ cos(t), -sin(t) ],
    #  [ sin(t),  cos(t) ]]

    angle = math.radians(degrees)
    new_x = math.cos(angle) * x - math.sin(angle) * y
    new_y = math.sin(angle) * x + math.cos(angle) * y

    return new_x, new_y


@_plot_hs.register
def _plot_hp(hp: Hp, ax: plt.Axes, xlim, ylim):
    lines = _plot_hs_line(hp, ax, xlim, ylim, linestyle=":")
    _plot_hs_arrow(hp, ax, color=lines[0].get_color())


@_plot_hs.register
def _plot_hpc(hpc: Hpc, ax: plt.Axes, xlim, ylim):
    lines = _plot_hs_line(hpc, ax, xlim, ylim, linestyle="-")
    _plot_hs_arrow(hpc, ax, color=lines[0].get_color())


def _plot_hs_line(hs: Hs, ax: plt.Axes, xlim, ylim, linestyle: str):
    x1 = xlim[0] - 1
    x2 = xlim[1] + 1

    y1 = hs.y(x1)
    y2 = hs.y(x2)

    if y1 is None or y2 is None:
        # This means we have a vertical line.
        x = hs[0][0]
        y1 = ylim[0] - 1
        y2 = ylim[1] + 1
        return ax.plot([x, x], [y1, y2], linestyle=linestyle)

    return ax.plot([x1, x2], [y1, y2], linestyle=linestyle)


def _plot_hs_arrow(hs: Hs, ax: plt.Axes, color: str):
    p1, p2 = [p.position for p in hs]

    delta = p2 - p1
    center = (p1 + p2) / 2
    delta_normalized = delta / np.linalg.norm(delta)

    # We're assuming that both Hp & Hpc both represent the points "on the left"
    # of the line.
    angle = 90

    ax.arrow(
        *center[:2],
        *_rotate_vector(*delta_normalized[:2], angle),
        width=0.1,
        color=color,
    )


def _plot_esum(esum: Esum, ax, xlim, ylim):
    datapoints = _datapoints(
        esum,
        np.arange(xlim[0], xlim[1], 0.5),
        np.arange(ylim[0], ylim[1], 0.5),
    )

    contains_col = datapoints[:, 2] > 0.5
    (ones_ind,) = np.where(contains_col)
    (zeroes_ind,) = np.where(~contains_col)

    ax.scatter(datapoints[:, 0][zeroes_ind], datapoints[:, 1][zeroes_ind], alpha=0.1)
    ax.scatter(datapoints[:, 0][ones_ind], datapoints[:, 1][ones_ind])

    locator = matplotlib.ticker.MaxNLocator(integer=True)
    ax.xaxis.set_major_locator(locator)
    ax.yaxis.set_major_locator(locator)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")

    for term in esum.terms:
        for hs in term:
            _plot_hs(hs, ax, xlim, ylim)


def main():
    esum1 = Esum(
        {
            frozenset(
                [
                    # vertical line (|)
                    Hp(
                        Pt(1, 6),
                        Pt(1, 1),
                    ),
                    # horizontal line (-)
                    Hpc(
                        Pt(2, 2),
                        Pt(8, 2),
                    ),
                    # diagonal line (\)
                    Hp(
                        Pt(15, 1),
                        Pt(0, 16),
                    ),
                    # horizontal line (-)
                    Hp(
                        Pt(11, 10),
                        Pt(4, 10),
                    ),
                ]
            )
        }
    )

    esum2 = Esum(
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
                ]
            )
        }
    )

    fig, axes = plt.subplots(3, 2, figsize=(24, 36))
    xlim = [0, 20]
    ylim = [0, 20]

    _plot_esum(esum1, axes[0][0], xlim, ylim)
    axes[0][0].set_title("$ e_1 $")

    _plot_esum(esum2, axes[0][1], xlim, ylim)
    axes[0][1].set_title("$ e_2 $")

    _plot_esum(esum1.union(esum2), axes[1][0], xlim, ylim)
    axes[1][0].set_title("$ e_1 \\cup e_2 $")

    _plot_esum(esum1.intersection(esum2), axes[1][1], xlim, ylim)
    axes[1][1].set_title("$ e_1 \\cap e_2 $")

    _plot_esum(esum2.conjugate, axes[2][0], xlim, ylim)
    axes[2][0].set_title("$ \\overline{e_2} $")

    _plot_esum(esum1.difference(esum2), axes[2][1], xlim, ylim)
    axes[2][1].set_title("$ e_1 \\backslash e_2 $")

    plot_path = Path("./plots/output.pdf")
    plot_path.parent.mkdir(exist_ok=True)

    fig.savefig(plot_path)


if __name__ == "__main__":
    main()
