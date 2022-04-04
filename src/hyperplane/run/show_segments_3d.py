from pathlib import Path
import typing as t

import matplotlib.pyplot as plt

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/segments_3d")


def _draw_segments_3d(ax, segments: t.Sequence[flat.CrossSegment], xlim, ylim):
    ax.azim = -90
    ax.elev = 70

    for segment_i, segment in enumerate(segments):
        x1, y1, _ = segment.x1.point.position
        x2, y2, _ = segment.x2.point.position
        # text = str(segment_i)

        ax.plot([x1, x2], [y1, y2], [segment_i, segment_i], c="C1", alpha=0.3)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)


def _plot(esum, vertices, segments, path, name):
    fig = plt.figure(dpi=400)
    axes = fig.gca(projection="3d")

    xlim = [0, 20]
    ylim = [0, 20]

    _draw_segments_3d(axes, segments, xlim, ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.letter_c()]):
        vertices = flat.find_vertices(esum=esum)
        segments = flat.segments(vertices)

        _plot(
            esum=esum,
            vertices=vertices,
            segments=segments,
            path=RESULTS_PATH / f"shape_{shape_i}.png",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
