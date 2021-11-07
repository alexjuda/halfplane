import matplotlib.pyplot as plt
import numpy as np

from hyperplane import flat2


def _sample_line(line: flat2.Line) -> np.ndarray:
    xs = np.array([-3, 0, 3])
    ys = line.a * xs + line.b
    return np.vstack((xs, ys)).T


# TODO:
# def _halfspace_patch()


def main():
    fig, ax = plt.subplots()

    shape = flat2.Triangle(
        (
            flat2.Halfplane(flat2.Line(1, 0), flat2.Op.GREATER_THAN),
            flat2.Halfplane(flat2.Line(2, 0), flat2.Op.LESS_THAN),
            flat2.Halfplane(flat2.Line(-1, 4), flat2.Op.LESS_THAN),
        )
    )

    for halfplane in shape.halfplanes:
        line_samples = _sample_line(halfplane.line)
        ax.plot(
            line_samples[:, 0],
            line_samples[:, 1],
            color=(0, 0, 0.8, 0.5),
        )

    vertices = shape.vertices
    ax.scatter(
        vertices[:, 0],
        vertices[:, 1],
        color="gray",
    )


    # Make the axis arrows cross at the center
    # src: https://matplotlib.org/stable/gallery/ticks_and_spines/spine_placement_demo.html
    ax.spines.left.set_position("zero")
    ax.spines.bottom.set_position("zero")
    ax.spines.right.set_color("none")
    ax.spines.top.set_color("none")

    # ax.set_xlim([-10, 10])
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    main()
