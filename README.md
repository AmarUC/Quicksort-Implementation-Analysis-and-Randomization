# Quicksort-Implementation-Analysis-and-Randomization
This submission contains two in-place Python Quicksort implementations, a reproducible benchmark, measured results, and a report explaining the algorithms and their performance.

## Files

- `quicksort.py` — deterministic last-element-pivot and randomized-pivot implementations.
- `benchmark.py` — measures both algorithms on random, sorted, and reverse-sorted inputs; checks sorted output; writes CSV results.
- `benchmark_results.csv` — results from the run described in `report.md`.
- `report.md` — implementation notes, complexity analysis, methodology, results, and interpretation.

## Run

Requires Python 3.9 or later and no third-party packages. From this directory:

```bash
python benchmark.py
```

By default, the benchmark uses sizes 500, 1,000, 2,000, and 4,000, five timed repetitions per case, and seed 2026. Override these options as needed:

```bash
python benchmark.py --sizes 1000 5000 10000 --repeats 7 --seed 42 --output results.csv
```

To use the implementations directly:

```python
from quicksort import quicksort, randomized_quicksort

items = [8, 3, 5, 3, 1]
quicksort(items)  # sorts items in place and returns the same list

other_items = [8, 3, 5, 3, 1]
randomized_quicksort(other_items, seed=42)
```

## Summary

Both implementations use Lomuto partitioning. The deterministic version always uses the rightmost value as pivot, so already sorted and reverse-sorted input cause quadratic work. Randomized Quicksort chooses a uniformly random pivot and has expected `O(n log n)` time regardless of the input's original ordering, while retaining `O(n^2)` worst-case time. The benchmark results and caveats are in `report.md`.
