import matplotlib.pyplot as plt
import numpy as np

import hyperplane.flat as hp


def main():
    rect1 = hp.Rectangle(
        3,
        4,
    )
    rect2 = hp.Translation(2, -1, rect1)
    rect3 = hp.Translation(2, 0.5, rect2)
    solid = hp.Group(
        [
            rect1,
            rect2,
            rect3,
            hp.Rotation(3.14 / 6, rect3),
        ]
    )

    fig, ax = plt.subplots()
    for transform, shape in hp.iter_shapes(solid):
        points = transform.apply(shape.points())
        looped = np.hstack((points, points[:, :1]))

        ax.plot(
            looped[0, :],
            looped[1, :],
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
