from pathlib import Path
from pprint import pp

from .. import flat, shape_gen

RESULTS_PATH = Path("./data/segments")


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate(
        [
            shape_gen.play_button_shape(min_x=4.0, min_y=3.0, width=10.0, height=6.0),
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

        pp(
            {
                "esum": esum.debug_name,
                "n_terms": len(esum.eterms),
                "total_n_hses": len([hs for eterm in esum.eterms for hs in eterm.hses]),
                "n_vertices": len(vertices),
                "n_segments": len(segments),
                "n_boundary_segments": len(boundary_segments),
            }
        )


if __name__ == "__main__":
    main()
