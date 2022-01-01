import functools

import matplotlib.pyplot as plt
import numpy as np

from .flat import Hp, Hpc, Pt, Hs


def _pixel_mask(hs: Hs, x_iter, y_iter) -> np.ndarray:
    return np.array([[hs.contains(Pt(x, y)) for x in x_iter] for y in y_iter])


@functools.singledispatch
def _plot_hs(hs, ax: plt.Axes):
    raise NotImplementedError()


@_plot_hs.register
def _plot_hp(hp: Hp, ax: plt.Axes):
    ax.plot(
        [hp[0][0], hp[1][0]],
        [hp[0][1], hp[1][1]],
        line=":",
    )


@_plot_hs.register
def _plot_hpc(hpc: Hpc, ax: plt.Axes):
    ax.plot(
        [hpc[0][0], hpc[1][0]],
        [hpc[0][1], hpc[1][1]],
    )


def main():
    # hs = Hp(Pt(3, 5), Pt(9, 5))
    # hs = Hp(Pt(1, 1), Pt(4, 1))
    # hs = Hp(Pt(1, 6), Pt(4, 6))
    # hs = Hp(Pt(1, 6), Pt(8, 8))
    hs = Hpc(Pt(1, 6), Pt(8, 8))

    fig, ax = plt.subplots()
    ax.imshow(_pixel_mask(hs, range(20), range(20)), origin="lower")

    _plot_hs(hs, ax)

    plt.show()


if __name__ == "__main__":
    main()
