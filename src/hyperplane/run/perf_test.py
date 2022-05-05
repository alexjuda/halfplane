import csv
import time
from pathlib import Path

from tqdm import tqdm

from .. import flat, shape_gen


RESULTS_PATH = Path("./data/perf")


def main():
    RESULTS_PATH.mkdir(parents=True, exist_ok=True)

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

            writer.writerow(
                {
                    "generator": esum.debug_name,
                    "n_subshapes": n,
                    "delta_t": end_t - start_t,
                    "n_segments": len(segments),
                }
            )


if __name__ == "__main__":
    main()
