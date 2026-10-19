"""Reproducible timing comparison for the two Quicksort implementations."""

import argparse
import csv
import platform
import random
import statistics
import time
from pathlib import Path

from quicksort import quicksort, randomized_quicksort


def make_input(kind: str, n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randrange(n * 10 + 1) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    raise ValueError(kind)


def measure(sorter, data: list[int], repeats: int, seed: int) -> float:
    samples = []
    expected = sorted(data)
    for rep in range(repeats):
        work = data.copy()
        start = time.perf_counter()
        if sorter is randomized_quicksort:
            sorter(work, seed=seed + rep)
        else:
            sorter(work)
        samples.append(time.perf_counter() - start)
        if work != expected:
            raise RuntimeError(f"{sorter.__name__} returned incorrect result")
    return statistics.median(samples)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=[500, 1000, 2000, 4000])
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", type=Path, default=Path("benchmark_results.csv"))
    args = parser.parse_args()
    if args.repeats < 1 or any(n < 0 for n in args.sizes):
        parser.error("repeats must be positive and sizes nonnegative")

    rows = []
    for n in args.sizes:
        for distribution in ("random", "sorted", "reverse"):
            data = make_input(distribution, n, args.seed)
            for name, sorter in (("deterministic", quicksort), ("randomized", randomized_quicksort)):
                seconds = measure(sorter, data, args.repeats, args.seed)
                rows.append({"distribution": distribution, "n": n, "algorithm": name,
                             "median_seconds": f"{seconds:.9f}"})
                print(f"{distribution:7} n={n:6} {name:13} {seconds:.6f} s")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["distribution", "n", "algorithm", "median_seconds"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nPython {platform.python_version()} on {platform.platform()}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
