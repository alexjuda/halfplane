import matplotlib.pyplot as plt
import numpy as np

import hyperplane.flat as hp


def main():
    solid = hp.Translation(
        0,
        0,
        hp.Rotation(
            3.14 / 6,
            hp.Translation(
                0,
                1,
                hp.Rectangle(
                    3,
                    4,
                ),
            ),
        ),
    )

    fig, ax = plt.subplots()
    for transform, shape in hp.iter_shapes(solid):
        transformed_points = transform.A @ shape.points()
        transformed_points[0] += transform.b[0]
        transformed_points[1] += transform.b[1]

        looped = np.hstack((transformed_points, transformed_points[:, :1]))

        ax.plot(
            looped[0, :],
            looped[1, :],
        )
    plt.show()


if __name__ == "__main__":
    main()
