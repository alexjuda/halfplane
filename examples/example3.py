"""
Demonstration of an example usage.

Input: a shape defined using datastructures from the library.

Output: a plot of the inferred shape boundary.
"""
import typing as t
import matplotlib.pyplot as plt

from hyperplane.flat import Pt, Hpc, Eterm, Esum, XSegment, detect_boundary
from hyperplane import plots


def main():
    # 1. Define shapes
    triangle1 = Esum.from_terms(
        Eterm.from_hses(
            # diagonal line (/)
            Hpc(
                Pt(8, 10),
                Pt(3, 1),
            ),
            # diagonal line (\)
            Hpc(
                Pt(9, 1),
                Pt(4, 10),
            ),
            # horizontal line (-)
            Hpc(
                Pt(2, 2),
                Pt(10, 2),
            ),
        ),
    )

    triangle2 = Esum.from_terms(
        Eterm.from_hses(
            # diagonal line (/)
            Hpc(
                Pt(10, 10),
                Pt(5, 1),
            ),
            # diagonal line (\)
            Hpc(
                Pt(11, 1),
                Pt(6, 10),
            ),
            # horizontal line (-)
            Hpc(
                Pt(4, 2),
                Pt(12, 2),
            ),
        ),
    )

    # 2. Combine shapes using CSG operations

    combined_shape = triangle1.union(triangle2)
    # combined_shape = triangle1.intersection(triangle2)

    # 3. Run the algorithm - boundary detection
    boundary_segments = detect_boundary(combined_shape)

    # 4. Plot the detected boundary
    _plot(combined_shape, boundary_segments)


def _plot(shape: Esum, segments: t.Sequence[XSegment]):
    fig, axes = plots.subplots(2, 1, size=12)

    xlim = [0, 14]
    ylim = [0, 14]

    plots.plot_esum_boundaries(shape, ax=axes[0], xlim=xlim, ylim=ylim)
    axes[0].set_title("Halfspaces")

    plots.draw_segments(axes[1], segments, xlim, ylim, seg_ids=False)
    axes[1].set_title("Boundary")

    plt.show()


if __name__ == "__main__":
    main()
