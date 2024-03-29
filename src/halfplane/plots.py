import functools
import math
import typing as t
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

from . import flat
from .flat import X, Esum, Hp, Hpc, Hs, Pt


def _datapoints(esum: Esum, x_iter, y_iter) -> np.ndarray:
    """Returns [X*Y x 3] array of data point rows, where:
    - col 0: x coordinate
    - col 1: y coordinate
    - col 2: inside esum or not (bool)
    """
    return np.array([[x, y, esum.contains(Pt(x, y))] for x in x_iter for y in y_iter])


@functools.singledispatch
def _plot_hs(hs, hs_label, ax: plt.Axes, xlim, ylim):
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
def _plot_hp(hp: Hp, hs_label, ax: plt.Axes, xlim, ylim):
    lines = _plot_hs_line(
        hs=hp,
        hs_label=hs_label,
        ax=ax,
        xlim=xlim,
        ylim=ylim,
        linestyle=":",
    )
    _plot_hs_arrows(hp, ax, color=lines[0].get_color())


@_plot_hs.register
def _plot_hpc(hpc: Hpc, hs_label, ax: plt.Axes, xlim, ylim):
    lines = _plot_hs_line(
        hs=hpc,
        hs_label=hs_label,
        ax=ax,
        xlim=xlim,
        ylim=ylim,
        linestyle="-",
    )
    _plot_hs_arrows(hpc, ax, color=lines[0].get_color())


def _plot_hs_line(hs: Hs, hs_label: str, ax: plt.Axes, xlim, ylim, linestyle: str):
    x1 = xlim[0] - 1
    x2 = xlim[1] + 1

    y1 = hs.y(x1)
    y2 = hs.y(x2)

    if y1 is None or y2 is None:
        # This means we have a vertical line.
        x = hs.p1.x
        y1 = ylim[0] - 1
        y2 = ylim[1] + 1
        return ax.plot([x, x], [y1, y2], linestyle=linestyle, label=hs_label)

    return ax.plot([x1, x2], [y1, y2], linestyle=linestyle, label=hs_label)


def _plot_hs_arrows(hs: Hs, ax: plt.Axes, color: str):
    p1, p2 = [p.position2d for p in [hs.p1, hs.p2]]

    delta = p2 - p1
    delta_normalized = delta / np.linalg.norm(delta)
    arrow_vector = delta_normalized[:2] * 0.4

    # We're assuming that both Hp & Hpc both represent the points "on the left"
    # of the line.
    angle = 90

    # Plot arrow at each control point. The arrows could be anywhere, but this
    # allows easier identification.
    ax.arrow(
        *p1[:2],
        *_rotate_vector(*arrow_vector, angle),
        width=0.1,
        color=color,
    )
    ax.arrow(
        *p2[:2],
        *_rotate_vector(*arrow_vector, angle),
        width=0.1,
        color=color,
    )


def _plot_esum_with_content_check(esum: Esum, ax, xlim, ylim):
    datapoints = _datapoints(
        esum,
        np.arange(xlim[0], xlim[1], 0.5),
        np.arange(ylim[0], ylim[1], 0.5),
    )

    contains_col = datapoints[:, 2] > 0.5
    (ones_ind,) = np.where(contains_col)
    (zeroes_ind,) = np.where(~contains_col)

    ax.scatter(
        datapoints[:, 0][zeroes_ind],
        datapoints[:, 1][zeroes_ind],
        alpha=0.1,
        label="miss",
    )
    ax.scatter(datapoints[:, 0][ones_ind], datapoints[:, 1][ones_ind], label="hit")

    locator = matplotlib.ticker.MaxNLocator(integer=True)
    ax.xaxis.set_major_locator(locator)
    ax.yaxis.set_major_locator(locator)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")

    plot_esum_boundaries(esum, ax, xlim, ylim)

    ax.legend(loc="upper right")


def draw_eterm(ax, eterm: flat.Eterm, xlim, ylim, clean=False):
    for hs_i, hs in enumerate(eterm.hses):
        label = hs.debug_name
        if clean:
            _plot_hpc(hs, hs_label=label, ax=ax, xlim=xlim, ylim=ylim)
        else:
            _plot_hs(hs, hs_label=label, ax=ax, xlim=xlim, ylim=ylim)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")

    if clean:
        ax.set_axis_off()
    else:
        locator = matplotlib.ticker.MaxNLocator(integer=True)
        ax.xaxis.set_major_locator(locator)
        ax.yaxis.set_major_locator(locator)
        ax.legend()


def plot_esum_boundaries(esum: Esum, ax, xlim, ylim, clean=False):
    for eterm in esum.eterms:
        draw_eterm(ax, eterm, xlim, ylim, clean=clean)


def subplots(n_rows, n_cols, size=12, **kwargs):
    return plt.subplots(
        n_rows,
        n_cols,
        figsize=(size * n_cols, size * n_rows),
        dpi=100,
        **kwargs,
    )


def _plot_point_by_point_check(esum1, esum2):
    fig, axes = subplots(3, 2)
    xlim = [0, 20]
    ylim = [0, 20]

    _plot_esum_with_content_check(esum1, axes[0][0], xlim, ylim)
    axes[0][0].set_title("$ e_1 $")

    _plot_esum_with_content_check(esum2, axes[0][1], xlim, ylim)
    axes[0][1].set_title("$ e_2 $")

    _plot_esum_with_content_check(esum1.union(esum2), axes[1][0], xlim, ylim)
    axes[1][0].set_title("$ e_1 \\cup e_2 $")

    _plot_esum_with_content_check(esum1.intersection(esum2), axes[1][1], xlim, ylim)
    axes[1][1].set_title("$ e_1 \\cap e_2 $")

    _plot_esum_with_content_check(esum2.conjugate, axes[2][0], xlim, ylim)
    axes[2][0].set_title("$ \\overline{e_2} $")

    _plot_esum_with_content_check(esum1.difference(esum2), axes[2][1], xlim, ylim)
    axes[2][1].set_title("$ e_1 \\backslash e_2 $")

    plot_path = Path("./plots/point_by_point_check.png")
    plot_path.parent.mkdir(exist_ok=True)

    fig.savefig(plot_path)


def _find_and_plot_vertices(esum: Esum, ax, xlim, ylim, draw_crosses_outside=True):
    halfspaces = [hs for term in esum.eterms for hs in term.hses]
    crosses = flat.find_all_xs(halfspaces)

    vertices = set()
    for cross in crosses:
        if esum.contains_cross(cross):
            vertices.add(cross)

    if draw_crosses_outside:
        crosses_outside = crosses.difference(vertices)
    else:
        crosses_outside = None

    draw_vertices(
        vertices=vertices,
        ax=ax,
        xlim=xlim,
        ylim=ylim,
        crosses_outside=crosses_outside,
    )

    ax.legend()


def draw_vertices(vertices: t.Sequence[X], ax, xlim, ylim, crosses_outside=None):
    plot_outside = crosses_outside is not None
    if plot_outside:
        ax.scatter(
            [cross.point.x for cross in crosses_outside],
            [cross.point.y for cross in crosses_outside],
            s=200,
            facecolors="none",
            edgecolors="C0",
            label="intersection point outside Esum",
        )

    color = "C1" if plot_outside else "C0"
    ax.scatter(
        [cross.point.x for cross in vertices],
        [cross.point.y for cross in vertices],
        s=200,
        facecolors=color,
        edgecolors=color,
        alpha=0.6,
        label="intersection point inside Esum",
    )
    ax.set_title("Vertex detection")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def _plot_all_crosses(esum: Esum, ax, xlim, ylim):
    halfspaces = [hs for term in esum.eterms for hs in term.hses]
    crosses = flat.find_all_xs(halfspaces)

    ax.scatter(
        [cross.point.x for cross in crosses],
        [cross.point.y for cross in crosses],
        s=200,
        facecolors="C1",
        edgecolors="C1",
    )


def _plot_point_check_and_crosses(esum, esum_name=None):
    fig, axes = subplots(1, 2)
    xlim = [0, 20]
    ylim = [0, 20]

    _plot_esum_with_content_check(esum, axes[0], xlim, ylim)
    axes[0].set_title("Point by point check")

    plot_esum_boundaries(esum, axes[1], xlim, ylim)

    _find_and_plot_vertices(esum, axes[1], xlim, ylim)

    plot_path = Path(f"./plots/vertices_{esum_name or ''}.png")
    plot_path.parent.mkdir(exist_ok=True)

    fig.savefig(plot_path)


def _plot_halfspaces_clean(esum: Esum, esum_name: str):
    fig, axes = subplots(1, 1, size=8)
    xlim = [0, 20]
    ylim = [0, 20]
    plot_esum_boundaries(esum, axes, xlim, ylim)
    axes.xaxis.set_major_locator(plt.NullLocator())
    axes.yaxis.set_major_locator(plt.NullLocator())

    plot_path = Path(f"./plots/hs_clean_{esum_name}.png")
    plot_path.parent.mkdir(exist_ok=True)
    fig.savefig(plot_path)


def _plot_vertices_clean(esum: Esum, esum_name: str):
    fig, axes = subplots(1, 1, size=8)
    xlim = [0, 20]
    ylim = [0, 20]
    plot_esum_boundaries(esum, axes, xlim, ylim)
    _find_and_plot_vertices(esum, axes, xlim, ylim, draw_crosses_outside=False)

    axes.set_title(None)
    axes.xaxis.set_major_locator(plt.NullLocator())
    axes.yaxis.set_major_locator(plt.NullLocator())
    axes.get_legend().remove()

    plot_path = Path(f"./plots/vertices_clean_{esum_name}.png")
    plot_path.parent.mkdir(exist_ok=True)
    fig.savefig(plot_path)


def _plot_all_crosses_clean(esum: Esum, esum_name: str):
    fig, axes = subplots(1, 1, size=8)
    xlim = [0, 20]
    ylim = [0, 20]
    plot_esum_boundaries(esum, axes, xlim, ylim)
    _plot_all_crosses(esum, axes, xlim, ylim)

    axes.xaxis.set_major_locator(plt.NullLocator())
    axes.yaxis.set_major_locator(plt.NullLocator())

    plot_path = Path(f"./plots/all_crosses_clean_{esum_name}.png")
    plot_path.parent.mkdir(exist_ok=True)
    fig.savefig(plot_path)


def draw_segments(ax, segments: t.Sequence[flat.XSegment], xlim, ylim, seg_ids=True):
    for segment_i, segment in enumerate(segments):
        x1, y1 = segment.x1.point.position2d
        x2, y2 = segment.x2.point.position2d

        ax.plot([x1, x2], [y1, y2], c="C1")

        if seg_ids:
            text = segment.debug_name or str(segment_i)
            ax.text(
                x=x1,
                y=y1,
                s=text,
                alpha=0.3,
                verticalalignment="bottom",
            )
            ax.text(
                x=x2,
                y=y2,
                s=text,
                alpha=0.3,
                verticalalignment="top",
            )
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")


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

    esum3 = Esum(
        {
            frozenset(
                [
                    # diagonal line (/)
                    Hpc(
                        Pt(8, 10),
                        Pt(4, 2),
                    ),
                    # diagonal line (\)
                    Hpc(
                        Pt(12, 2),
                        Pt(10, 10),
                    ),
                    # horizontal line (-)
                    Hpc(
                        Pt(2, 2),
                        Pt(8, 2),
                    ),
                ]
            )
        }
    )
    # _plot_point_by_point_check(esum1, esum2)
    _find_and_plot_vertices(esum1.intersection(esum2))

    # _plot_halfspaces_clean(esum1, "e1")
    # _plot_halfspaces_clean(esum2, "e2")
    # _plot_halfspaces_clean(esum1.intersection(esum2), "e3")
    # _plot_vertices_clean(esum1.intersection(esum2), "e3")
    # _plot_all_crosses_clean(esum1.intersection(esum2), "e3")
    breakpoint()


if __name__ == "__main__":

    main()
