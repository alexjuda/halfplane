import more_itertools as mitt
from pathlib import Path
import numpy as np

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/phases")


def _plot(esum, path, name):
    xlim = ylim = [-2, 14]

    vertices = flat.find_vertices(esum)

    fig, axes = plots.subplots(1 + len(vertices), 2)
    plots.plot_esum_boundaries(esum, ax=axes[0][0], xlim=xlim, ylim=ylim)

    plots.draw_vertices(vertices, ax=axes[0][1], xlim=xlim, ylim=ylim)

    index = flat.hs_crosses_index(vertices)
    for x_i, x_of_interest in enumerate(vertices):
        hs_segments = []
        for hs in x_of_interest.halfspaces:
            # 1. get neighbors for p1.hs1, p1.hs2
            # We need to retain order.
            xs_on_this_hs = list(index[hs])
            if len(xs_on_this_hs) <= 1:
                continue

            # 2. order by HS direction
            # Solution:
            # - pick any x1 and x2
            # - treat x1 as the coordinate origin
            # - treat <x1 x2> vector as the reference vector
            # - for all xs make vectors anchored at x1
            # - for all vectors compute the length of their projection on <x1 x2>
            # - sort points by the corresponding vector's projection lenth

            ref_x, *rest_xs = xs_on_this_hs
            ref_v = rest_xs[0].point.position - ref_x.point.position

            xs_sorted = sorted(
                xs_on_this_hs,
                key=lambda x: np.dot(x.point.position - ref_x.point.position, ref_v),
            )

            # 3. Connect subsequent pairs to get the smallest segments
            segments = [
                flat.CrossSegment(x1, x2) for x1, x2 in mitt.windowed(xs_sorted, n=2)
            ]
            hs_segments.append(segments)

            # TODO: classify segments
        plots.draw_segments(
            ax=axes[x_i + 1][0], segments=hs_segments[0], xlim=xlim, ylim=ylim
        )
        plots.draw_segments(
            ax=axes[x_i + 1][1], segments=hs_segments[1], xlim=xlim, ylim=ylim
        )

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.crude_c()]):
        _plot(
            esum=esum,
            path=RESULTS_PATH / f"shape_{shape_i}.pdf",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
