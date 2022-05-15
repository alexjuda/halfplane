import csv
import time
from pathlib import Path

import numpy as np
import numpy.polynomial
from tqdm import tqdm

from hyperplane import flat, shape_gen, plots


RESULTS_PATH = Path("./data/perf")


def _format_coef(coef):
    c0, *rest_cs = coef
    return ", ".join(f"$ {c:.2f}x^{c_i} $" for c_i, c in enumerate(coef))


def _plot_complexity(records, path):
    fig, ax = plots.subplots(1, 1)

    ns = np.array([int(r["n_subshapes"]) for r in records])
    delta_ts = np.array([float(r["delta_t"]) for r in records])

    ax.plot(
        ns,
        delta_ts,
        label="measured",
    )

    coef_2 = np.polynomial.polynomial.polyfit(ns, delta_ts, deg=2)
    coef_3 = np.polynomial.polynomial.polyfit(ns, delta_ts, deg=3)

    # (x - 10)(x - 20) = x^2 - 30x + 200
    # coef_2 = np.array([200, -30, 1])

    poly_xs = np.linspace(0, np.max(ns), 20)

    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_2),
        label=f"quadratic interpolation ({_format_coef(coef_2)})",
    )

    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_3),
        label=f"cubic interpolation ({_format_coef(coef_3)})",
    )

    ax.set_title("Time complexity, rect_chain")
    ax.set_xlabel("n rectangles")
    ax.set_ylabel("time [s]")
    ax.legend()

    fig.savefig(path)


def main():
    RESULTS_PATH.mkdir(parents=True, exist_ok=True)

    data_rows = []

    with open(RESULTS_PATH / "result.csv", "w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "generator",
                "n_subshapes",
                "delta_t",
                "n_segments",
            ],
        )
        writer.writeheader()

        for n in tqdm(range(5, 55, 5), desc="n"):
            esum = shape_gen.rect_chain(n=n)

            start_t = time.time()
            segments = flat.detect_segments(esum)
            end_t = time.time()

            data_row = {
                "generator": esum.debug_name,
                "n_subshapes": n,
                "delta_t": end_t - start_t,
                "n_segments": len(segments),
            }

            writer.writerow(data_row)
            data_rows.append(data_row)

    with open(RESULTS_PATH / "result.csv") as f:
        data_rows = list(csv.DictReader(f))

    _plot_complexity(data_rows, RESULTS_PATH / "result.png")


if __name__ == "__main__":
    main()