import functools
import math
import typing as t

import matplotlib.pyplot as plt
import numpy as np

from .flat import Hp, Hpc, Pt, Hs, Esum


def _hs_pixel_mask(hs: Hs, x_iter, y_iter) -> np.ndarray:
    return np.array([[hs.contains(Pt(x, y)) for x in x_iter] for y in y_iter])


def _pixel_mask(esum: Esum, x_iter, y_iter) -> np.ndarray:
    return np.array([[esum.contains(Pt(x, y)) for x in x_iter] for y in y_iter])


@functools.singledispatch
def _plot_hs(hs, ax: plt.Axes):
    raise NotImplementedError()


def _rotate_vector(x: float, y: float, degrees) -> t.Tuple[float, float]:
    # Rotation matrix is:
    # [[ cos(t), -sin(t) ],
    #  [ sin(t),  cos(t) ]]

    angle = math.radians(degrees)
    new_x = math.cos(angle) * x - math.sin(angle) * y
    new_y = math.sin(angle) * x + math.cos(angle) * y

    return new_x, new_y


@_plot_hs.register
def _plot_hp(hp: Hp, ax: plt.Axes):
    ax.plot(
        [hp[0][0], hp[1][0]],
        [hp[0][1], hp[1][1]],
        linestyle=":",
    )
    _plot_hs_arrow(hp, ax, -90)


@_plot_hs.register
def _plot_hpc(hpc: Hpc, ax: plt.Axes):
    ax.plot(
        [hpc[0][0], hpc[1][0]],
        [hpc[0][1], hpc[1][1]],
    )
    _plot_hs_arrow(hpc, ax, 90)


def _plot_hs_arrow(hs: Hs, ax: plt.Axes, angle):
    p1, p2 = [p.position for p in hs]

    delta = p2 - p1
    center = (p1 + p2) / 2
    delta_normalized = delta / np.linalg.norm(delta)

    ax.arrow(
        *center[:2],
        *_rotate_vector(*delta_normalized[:2], angle),
        width=0.1,
    )


def main():
    # hs = Hp(Pt(3, 5), Pt(9, 5))
    # hs = Hp(Pt(1, 1), Pt(4, 1))
    # hs = Hp(Pt(1, 6), Pt(4, 6))
    # hs = Hp(Pt(1, 6), Pt(8, 8))
    # hs = Hpc(Pt(1, 6), Pt(8, 8))

    esum = Esum(
        {
            frozenset(
                [
                    # vertical line (|)
                    Hp(
                        Pt(1, 1),
                        Pt(1, 6),
                    ),
                    # horizontal line (-)
                    Hpc(
                        Pt(2, 2),
                        Pt(8, 2),
                    ),
                    # diagonal line (\)
                    Hp(
                        Pt(0, 16),
                        Pt(14, 1),
                    ),
                    # horizontal line (-)
                    Hp(
                        Pt(4, 10),
                        Pt(11, 10),
                    ),
                ]
            )
        }
    )

    fig, ax = plt.subplots()

    ax.imshow(_pixel_mask(esum, range(20), range(20)), origin="lower")

    for term in esum.terms:
        for hs in term:
            _plot_hs(hs, ax)

    plt.show()


if __name__ == "__main__":
    main()
