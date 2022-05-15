import dataclasses
import typing as t
from pathlib import Path

import pandas as pd
import plotly.express as px

from .. import common_shapes, flat, shape_gen

RESULTS_PATH = Path("./data/segments_3d")


def _draw_segments_3d(ax, segments: t.Sequence[flat.XSegment], xlim, ylim):
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
    n_segments = len(segments)
    for segment_i, segment in enumerate(segments):
        x1, y1, _ = segment.x1.point.position
        x2, y2, _ = segment.x2.point.position

        rows.extend(
            [
                {
                    "x": x1,
                    "y": y1,
                    "z": segment_i / n_segments,
                    "segment_name": segment.debug_name,
                    "point_name": segment.x1.debug_name,
                    "hs1_name": segment.x1.hs1.debug_name,
                    "hs2_name": segment.x1.hs2.debug_name,
                },
                {
                    "x": x2,
                    "y": y2,
                    "z": segment_i / n_segments,
                    "segment_name": segment.debug_name,
                    "point_name": segment.x2.debug_name,
                    "hs1_name": segment.x2.hs1.debug_name,
                    "hs2_name": segment.x2.hs2.debug_name,
                },
            ]
        )

    df = pd.DataFrame.from_records(rows)

    fig = px.line_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="segment_name",
        hover_name="point_name",
        hover_data=["hs1_name", "hs2_name"],
    )
    fig.write_html(path)


def _named(seq: t.Sequence, prefix: str) -> t.Sequence:
    return [
        dataclasses.replace(item, debug_name=f"{prefix}_{i}")
        for i, item in enumerate(seq)
    ]


def _with_name(obj, new_name):
    return dataclasses.replace(obj, debug_name=new_name)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum_start in enumerate(
        [
            common_shapes.letter_c(),
            shape_gen.rect_chain(n=4, stride_x=3, stride_y=3),
            shape_gen.rect_chain(n=10, stride_x=3, stride_y=3),
        ]
    ):
        esum = flat.named_esum(esum_start)
        vertices = _named(flat.find_vertices(esum=esum), "x")
        segments = _named(flat.find_segments(vertices), "seg")
        boundary_segments = flat.filter_segments(esum, segments)

        _plot(
            esum=esum,
            vertices=vertices,
            segments=boundary_segments,
            path=RESULTS_PATH / f"shape_{shape_i}.html",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
