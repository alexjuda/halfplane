from pathlib import Path

import more_itertools as mitt
import pandas as pd
import plotly.express as px

from .. import common_shapes, flat


RESULTS_PATH = Path("./data/lines_3d")


def _plot(esum: flat.Esum, path, name):
    rows = []
    all_hses = list(mitt.unique_everseen(hs for term in esum.terms for hs in term))

    for hs_i, hs in enumerate(all_hses):
        x1, y1 = hs.p1.position2d
        x2, y2 = hs.p2.position2d

        rows.extend(
            [
                {
                    "x": x1,
                    "y": y1,
                    "z": hs_i / len(all_hses),
                    "hs_name": hs.debug_name,
                    "point_name": hs.p1.debug_name,
                },
                {
                    "x": x2,
                    "y": y2,
                    "z": hs_i / len(all_hses),
                    "hs_name": hs.debug_name,
                    "point_name": hs.p2.debug_name,
                },
            ]
        )

    df = pd.DataFrame.from_records(rows)

    fig = px.line_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="hs_name",
        hover_name="point_name",
    )
    fig.write_html(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum_start in enumerate([common_shapes.letter_c()]):
        esum = flat.named_esum(esum_start)

        _plot(
            esum=esum,
            path=RESULTS_PATH / f"shape_{shape_i}.html",
            name=esum.name,
        )


if __name__ == "__main__":
    main()
