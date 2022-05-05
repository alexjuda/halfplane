import csv
import time
from pathlib import Path

from tqdm import tqdm

from .. import flat, shape_gen, plots


RESULTS_PATH = Path("./data/perf")


def _plot_complexity(records, path):
    fig, ax = plots.subplots(1, 1)

    ax.plot(
        [int(r["n_subshapes"]) for r in records], [float(r["delta_t"]) for r in records]
    )

    ax.set_title("Time complexity, rect_chain")
    ax.set_xlabel("n rectangles")
    ax.set_ylabel("time [s]")

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

    # with open(RESULTS_PATH / "result.csv") as f:
    #     data_rows = list(csv.DictReader(f))

    _plot_complexity(data_rows, RESULTS_PATH / "result.png")


if __name__ == "__main__":
    main()
