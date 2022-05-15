# Running:
# python -m cProfile -o plain.profile -m hyperplane.run.perf.plain_detect 10
from argparse import ArgumentParser

from hyperplane import flat, shape_gen


def main():
    parser = ArgumentParser()
    parser.add_argument("n", type=int, help="Size of the rect chain")
    args = parser.parse_args()

    esum = shape_gen.rect_chain(n=args.n)
    segments = flat.detect_segments(esum)
    print(f"Detected {len(segments)} segments")


if __name__ == "__main__":
    main()
