import typing as t
from pathlib import Path

from .. import flat
from .. import plots
from .. import common_shapes


RESULTS_PATH = Path("./data/segments")


def _draw_segments(ax, segments: t.Sequence[flat.CrossSegment]):
    for segment_i, segment in enumerate(segments):
        x1, y1, _ = segment.x1.point.position
        x2, y2, _ = segment.x2.point.position
        text = str(segment_i)

        ax.plot([x1, x2], [y1, y2], c="C1")
        ax.text(
            x=(x1 + x2) / 2,
            y=(y1 + y2) / 2,
            s=text,
        )


def _plot(esum, vertices, segments, path, name):
    fig, axes = plots.subplots(1, 2)

    xlim = [0, 20]
    ylim = [0, 20]

    plots.plot_esum_boundaries(esum, ax=axes[0], xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=axes[0], xlim=xlim, ylim=ylim)
    axes[0].set_title(name)

    _draw_segments(axes[1], segments)

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
