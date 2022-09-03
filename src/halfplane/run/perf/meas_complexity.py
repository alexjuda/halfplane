"""
Runs a series of experiments with shape generator, measures the execution time,
and stores the results in a csv. The generator is 'rect_chain'. At the end,
plots the time complexity chart.
"""

import csv
import time
from pathlib import Path

import numpy as np
import numpy.polynomial
from tqdm import tqdm

from halfplane import flat, shape_gen, plots


RESULTS_PATH = Path("./data/perf")


def _format_coef(coef):
    c0, *rest_cs = coef
    return ", ".join(f"$ {c:.2f}x^{c_i} $" for c_i, c in enumerate(coef))


def _mse(x, ref_y, poly_coef):
    pred_y = np.polynomial.polynomial.polyval(x, poly_coef)
    mse = np.mean((pred_y - ref_y) ** 2)
    return mse


def _plot_complexity(records, path):
    fig, ax = plots.subplots(1, 1)

    ns = np.array([int(r["n_subshapes"]) for r in records])
    delta_ts = np.array([float(r["delta_t"]) for r in records])

    ax.scatter(
        ns,
        delta_ts,
        label="measured",
    )

    coef_1 = np.polynomial.polynomial.polyfit(ns, delta_ts, deg=1)
    coef_2 = np.polynomial.polynomial.polyfit(ns, delta_ts, deg=2)
    coef_3 = np.polynomial.polynomial.polyfit(ns, delta_ts, deg=3)

    poly_xs = np.linspace(0, np.max(ns), 20)

    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_1),
        label=(
            f"linear interpolation ({_format_coef(coef_1)}), "
            f"MSE = {_mse(ns, delta_ts, coef_1):.1f}"
        ),
        color="C1",
    )
    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_2),
        label=(
            f"quadratic interpolation ({_format_coef(coef_2)}), "
            f"MSE = {_mse(ns, delta_ts, coef_2):.1f}"
        ),
        color="C2",
    )

    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_3),
        label=(
            f"cubic interpolation ({_format_coef(coef_3)}), "
            f"MSE = {_mse(ns, delta_ts, coef_3):.1f}"
        ),
        color="C3",
    )

    ax.set_title("Time complexity, rect_chain")
    ax.set_xlabel("n rectangles")
    ax.set_ylabel("time [s]")
    ax.legend()

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(parents=True, exist_ok=True)

    # data_rows = []

    # with open(RESULTS_PATH / "result.csv", "w") as f:
    #     writer = csv.DictWriter(
    #         f,
    #         fieldnames=[
    #             "generator",
    #             "n_subshapes",
    #             "delta_t",
    #             "n_segments",
    #         ],
    #     )
    #     writer.writeheader()

    #     for n in tqdm(range(5, 55, 5), desc="n"):
    #         esum = shape_gen.rect_chain(n=n)

    #         start_t = time.time()
    #         segments = flat.detect_boundary(esum)
    #         end_t = time.time()

    #         data_row = {
    #             "generator": esum.debug_name,
    #             "n_subshapes": n,
    #             "delta_t": end_t - start_t,
    #             "n_segments": len(segments),
    #         }

    #         writer.writerow(data_row)
    #         data_rows.append(data_row)

    with open(RESULTS_PATH / "result.csv") as f:
        data_rows = list(csv.DictReader(f))

    _plot_complexity(data_rows, RESULTS_PATH / "result.png")


if __name__ == "__main__":
    main()
