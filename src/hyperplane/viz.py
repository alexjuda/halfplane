import matplotlib.pyplot as plt
import matplotlib.patches

import hyperplane.flat as hp


def main():
    solid = hp.Rotation(
        3.14 / 6,
        hp.Translation(
            -3,
            -2,
            hp.Rectangle(
                3,
                4,
            ),
        ),
    )

    fig, ax = plt.subplots()
    ax.add_patch(
        matplotlib.patches.Rectangle(
            (0, 0),
            solid.width,
            solid.height,
            linewidth=1,
            edgecolor="b",
            facecolor="none",
        )
    )
    plt.show()


if __name__ == "__main__":
    main()
