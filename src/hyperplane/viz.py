import matplotlib.pyplot as plt
import matplotlib.patches

import hyperplane.flat as hp


def main():
    solid = hp.Rectangle(width=3, height=4)

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
