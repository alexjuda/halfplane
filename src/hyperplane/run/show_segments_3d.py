import dataclasses
from pathlib import Path
import typing as t

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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
    rows = []
    for segment_i, segment in enumerate(segments):
        x1, y1, _ = segment.x1.point.position
        x2, y2, _ = segment.x2.point.position

        rows.extend(
            [
                {
                    "x": x1,
                    "y": y1,
                    "segment_i": segment_i,
                    "segment_name": segment.debug_name,
                },
                {
                    "x": x2,
                    "y": y2,
                    "segment_i": segment_i,
                    "segment_name": segment.debug_name,
                },
            ]
        )

    df = pd.DataFrame.from_records(rows)

    fig = px.line_3d(df, x="x", y="y", z="segment_i", color="segment_name")
    fig.write_html(path)


def _named(seq: t.Sequence, prefix: str) -> t.Sequence:
    return [
        dataclasses.replace(item, debug_name=f"{prefix}_{i}")
        for i, item in enumerate(seq)
    ]


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate([common_shapes.letter_c()]):
        vertices = flat.find_vertices(esum=esum)
        segments = flat.segments(vertices)

        _plot(
            esum=esum,
            vertices=vertices,
            segments=_named(segments, "seg"),
            path=RESULTS_PATH / f"shape_{shape_i}.html",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
