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
import pandas as pd

from halfplane import flat, shape_gen, plots


ALL_RESULTS_PATH = Path("./data/perf")


def _format_coef(coef):
    c0, *rest_cs = coef
    return ", ".join(f"$ {c:.2f}x^{c_i} $" for c_i, c in enumerate(coef))


def _mse(x, ref_y, poly_coef):
    pred_y = np.polynomial.polynomial.polyval(x, poly_coef)
    mse = np.mean((pred_y - ref_y) ** 2)
    return mse


def _plot_complexity(data_df: pd.DataFrame, path):
    fig, ax = plots.subplots(1, 1)

    col_x = "n_subshapes"
    col_y = "delta_t"
    raw_df = data_df[[col_x, col_y]]

    ax.scatter(
        raw_df[col_x],
        raw_df[col_y],
        label="measured",
        color="C0",
    )

    median_df = raw_df.groupby("n_subshapes").median().reset_index()
    ax.plot(
        median_df[col_x],
        median_df[col_y],
        label="median for given $n$",
        color="C1",
    )

    coef_2 = np.polynomial.polynomial.polyfit(median_df[col_x], median_df[col_y], deg=2)
    coef_3 = np.polynomial.polynomial.polyfit(median_df[col_x], median_df[col_y], deg=3)

    poly_xs = np.linspace(0, np.max(median_df[col_x]), 20)

    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_2),
        label=(
            f"quadratic interpolation ({_format_coef(coef_2)}), "
            f"MSE = {_mse(median_df[col_x], median_df[col_y], coef_2):.2g}"
        ),
        color="C2",
    )

    ax.plot(
        poly_xs,
        np.polynomial.polynomial.polyval(poly_xs, coef_3),
        label=(
            f"cubic interpolation ({_format_coef(coef_3)}), "
            f"MSE = {_mse(median_df[col_x], median_df[col_y], coef_3):.2g}"
        ),
        color="C3",
    )

    ax.set_title("Time complexity of detect_boundary()")
    ax.set_xlabel("n rectangles")
    ax.set_ylabel("time [s]")
    ax.legend()

    fig.savefig(path)


def _plot_generic(
    records,
    x_name,
    y_name,
    path: Path,
    title=None,
    x_title=None,
    y_title=None,
    size=12,
):
    fig, ax = plots.subplots(1, 1, size=size)

    x = np.array([int(r[x_name]) for r in records])
    y = np.array([float(r[y_name]) for r in records])

    ax.plot(x, y, marker="o")

    if title is not None:
        ax.set_title(title)

    if x_title is not None:
        ax.set_xlabel(x_title)

    if y_title is not None:
        ax.set_ylabel(y_title)

    fig.savefig(path)


N_TRIALS = 5


def main():

    data_rows = []

    for generator_fn in [
        shape_gen.rect_union_chain,
        shape_gen.rect_intersection_chain,
    ]:
        generator_name = generator_fn.__name__
        print(f"Running generator {generator_name}")

        generator_results_path = ALL_RESULTS_PATH / generator_name
        generator_results_path.mkdir(parents=True, exist_ok=True)

        run = True
        if run:
            with open(generator_results_path / "result.csv", "w") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "generator",
                        "n_subshapes",
                        "delta_t",
                        "n_segments",
                        "n_eterms",
                        "n_halfspaces",
                    ],
                )
                writer.writeheader()

                for n in [*range(1, 5), *range(20, 140, 20)]:
                    for trial_i in tqdm(range(N_TRIALS), desc=f"{n=}, trial"):
                        esum = generator_fn(n=n)

                        start_t = time.time()
                        segments = flat.detect_boundary(esum)
                        end_t = time.time()

                        n_eterms = len(esum.eterms)
                        n_hses = sum(len(eterm.hses) for eterm in esum.eterms)

                        data_row = {
                            "generator": esum.debug_name,
                            "n_subshapes": n,
                            "delta_t": end_t - start_t,
                            "n_segments": len(segments),
                            "n_eterms": n_eterms,
                            "n_halfspaces": n_hses,
                        }

                        writer.writerow(data_row)
                        data_rows.append(data_row)

        with open(generator_results_path / "result.csv") as f:
            data_rows = list(csv.DictReader(f))

        data_df = pd.DataFrame.from_dict(data_rows).astype(
            {
                "n_subshapes": int,
                "delta_t": float,
                "n_eterms": int,
                "n_halfspaces": int,
            }
        )
        _plot_complexity(data_df, generator_results_path / "time_complexity.png")

        _plot_generic(
            data_rows,
            x_name="n_subshapes",
            y_name="n_eterms",
            title=(
                "Total number of eterms vs number of rectangles "
                "in the generated esum $e$"
            ),
            x_title="$n$",
            y_title="$|T(e)|$",
            size=8,
            path=generator_results_path / "n_eterms.png",
        )

        _plot_generic(
            data_rows,
            x_name="n_subshapes",
            y_name="n_halfspaces",
            title=(
                "Total number of halfspaces vs number of rectangles "
                "in the generated esum $e$"
            ),
            x_title="$n$",
            y_title=r"$\Sigma_{t \in T(e)} |H(t)|$",
            size=8,
            path=generator_results_path / "n_hses.png",
        )


if __name__ == "__main__":
    main()
