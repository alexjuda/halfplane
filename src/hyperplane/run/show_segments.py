from pathlib import Path
from pprint import pp

from .. import common_shapes, flat, plots, shape_gen

RESULTS_PATH = Path("./data/segments")


def _plot(esum, vertices, segments, path, name):
    fig, axes = plots.subplots(1, 2)

    xlim = [0, 20]
    ylim = [0, 20]

    plots.plot_esum_boundaries(esum, ax=axes[0], xlim=xlim, ylim=ylim)
    plots.draw_vertices(vertices, ax=axes[0], xlim=xlim, ylim=ylim)
    axes[0].set_title(name)

    plots.draw_segments(axes[1], segments, xlim, ylim)

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(exist_ok=True, parents=True)

    for shape_i, esum in enumerate(
        [
            # common_shapes.big_l(),
            # common_shapes.letter_c(),
            # shape_gen.rect_chain(n=4, stride_x=3, stride_y=3),
            shape_gen.play_button_shape(min_x=4.0, min_y=3.0, width=10.0, height=6.0),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=1, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=2, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=3, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=4, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=5, stride=0.2),
            shape_gen.play_button_chain(min_x=4.0, min_y=3.0, n=6, stride=0.2),
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

        # _plot(
        #     esum=esum,
        #     vertices=vertices,
        #     segments=boundary_segments,
        #     path=RESULTS_PATH / f"shape_{shape_i}.png",
        #     name=esum.name,
        # )


if __name__ == "__main__":
    main()
