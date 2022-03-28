import more_itertools as mitt
from pathlib import Path

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/phases")


def _plot(esum, path, name):
    fig, axes = plots.subplots(2, 2)

    xlim = ylim = [-2, 14]

    plots.plot_esum_boundaries(esum, ax=axes[0][0], xlim=xlim, ylim=ylim)

    vertices = flat.find_vertices(esum)
    index = flat.hs_crosses_index(vertices)
    x_of_interest = flat.query_cross(vertices, flat.Pt(10, 9))
    hs_segments = []
    for hs in x_of_interest.halfspaces:
        # 1. get neighbors for p1.hs1, p1.hs2
        # neighbor_xs = index[hs] - {x1}
        xs_on_this_hs = index[hs]

        # 2. order by HS direction
        # Solution: pick any x and sort all points on this HS by euclidean
        # distance from it.
        ref_x, *_ = xs_on_this_hs
        xs_seq = sorted(xs_on_this_hs, key=lambda x: x.point.distance(ref_x.point))

        # 3. Connect subsequent pairs to get the smallest segments
        segments = [flat.CrossSegment(x1, x2) for x1, x2 in mitt.windowed(xs_seq, n=2)]
        hs_segments.append(segments)

        # TODO: classify segments
    plots.draw_vertices(vertices, ax=axes[0][1], xlim=xlim, ylim=ylim)
    plots.draw_segments(ax=axes[1][0], segments=hs_segments[0], xlim=xlim, ylim=ylim)
    plots.draw_segments(ax=axes[1][1], segments=hs_segments[1], xlim=xlim, ylim=ylim)

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
