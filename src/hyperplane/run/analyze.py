import csv
from pathlib import Path
from pprint import pp

import more_itertools as mitt

from .. import flat, shape_gen

RESULTS_PATH = Path("./data/analysis")


def _dump_csv(f, rows):
    fields = list(mitt.unique_everseen(field for row in rows for field in row.keys()))
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    rows = []

    for shape_i, esum in enumerate(
        [
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=1, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=2, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=3, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=4, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=5, stride=0.2),
        ]
    ):
        vertices = flat.find_vertices(esum=esum)
        segments = flat.find_segments(vertices)
        boundary_segments = flat.filter_segments(esum, segments)

        row = {
            "esum": esum.debug_name,
            "n_terms": len(esum.eterms),
            "total_n_hses": len([hs for eterm in esum.eterms for hs in eterm.hses]),
            "n_vertices": len(vertices),
            "n_segments": len(segments),
            "n_boundary_segments": len(boundary_segments),
        }
        pp(row)
        rows.append(row)

    with open(RESULTS_PATH / "sizes.csv", "w") as f:
        _dump_csv(f, rows)


if __name__ == "__main__":
    main()
