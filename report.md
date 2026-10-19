# Quicksort: Implementation, Analysis, and Randomization

## 1. Design and implementation

`quicksort.py` provides two in-place algorithms for mutable sequences of values that support comparison:

1. **Deterministic Quicksort** selects the last element of each subarray as its pivot.
2. **Randomized Quicksort** uniformly selects an index in the current subarray, swaps that element to the end, and then uses the same partition routine.

Both use Lomuto partitioning. A boundary index tracks the end of values less than or equal to the pivot. The scan visits each other element once; values at most the pivot are moved to the left. Finally, the pivot is placed at the boundary. The pivot's final index separates the two ranges that remain to be sorted.

The functions sort the provided sequence in place and return that same sequence. The randomized function accepts an optional seed, which is useful for repeatable experiments. Equal values are supported. With this simple Lomuto scheme, equal values all go to the left side; consequently an all-equal input is a worst case. A three-way partition can improve duplicate-heavy inputs, but was intentionally omitted to keep the two pivot-selection strategies directly comparable.

Each implementation recursively sorts the smaller partition and iterates over the larger partition. This preserves the partition and comparison behavior while limiting the Python call stack to `O(log n)` even when the split is very unbalanced. It does not change the number of comparisons or the quadratic running time of bad pivots.

## 2. Time complexity

Partitioning a subarray of size `n` takes `Θ(n)` time. If a pivot leaves `k` elements on one side and `n-k-1` on the other, the recurrence is

`T(n) = T(k) + T(n-k-1) + Θ(n)`.

### Best case: `Θ(n log n)`

When each pivot divides the remaining elements into roughly equal halves, the recurrence is approximately `T(n) = 2T(n/2) + Θ(n)`. There are `Θ(log n)` levels of partitioning and each level processes `Θ(n)` total elements, giving `Θ(n log n)`.

### Average case: `Θ(n log n)`

For pivots that are uniformly distributed among the ranks, including when randomized pivot selection is used, expected partition sizes are sufficiently balanced over the recursion tree. Another view is that any pair of elements is compared at most once, and the probability that a pair is compared is `2/(j-i+1)` when their sorted ranks are `i < j`. Summing these probabilities gives expected comparisons `2(n+1)H_n - 4n = Θ(n log n)`, where `H_n` is the nth harmonic number. Thus the expected time is `Θ(n log n)`.

The conventional average-case bound for deterministic Quicksort assumes input order is random (or otherwise yields random-like pivot ranks). A fixed last-element pivot does not have this guarantee for every input distribution.

### Worst case: `Θ(n²)`

If each pivot is the smallest or largest remaining value, partitions have sizes `0` and `n-1`. The work is `n + (n-1) + ... + 1 = Θ(n²)`. With a last-element pivot this occurs on sorted and reverse-sorted inputs, and also on all-equal input under this implementation's `<=` partition rule. Randomized selection can also pick a sequence of extreme pivots, so randomization makes the worst case unlikely rather than impossible.

## 3. Space complexity and overhead

The code sorts in place, so the partitioning itself uses `O(1)` auxiliary storage. The smaller-side-recursion strategy bounds call-stack use by `O(log n)` for both implementations. A textbook direct recursive implementation can use `O(log n)` stack space in balanced cases and `O(n)` in the worst case; this implementation avoids that deep stack even though its comparison count may still be quadratic.

Randomized Quicksort additionally holds a pseudorandom-number generator and makes one random index selection per partition. That creates a small constant overhead, visible on small or already-random inputs. The benchmark times only the sort call; constructing the input, copying it, and checking correctness occur outside the timed interval.

## 4. Effect of randomization

For any fixed input, choosing a uniformly random pivot makes the pivot rank uniform among the current elements, so the expected running time is `Θ(n log n)` independent of whether the original sequence was sorted, reversed, or arranged adversarially for a fixed pivot rule. On distinct keys, the probability that every pivot along the whole sort is an extreme rank is `2^(n-1)/n!`, illustrating why one specific fully unbalanced path becomes unlikely as `n` grows. Randomization does not provide a hard worst-case guarantee, and duplicate-heavy data remains challenging for this two-way partition scheme.

## 5. Empirical analysis

### Method

`benchmark.py` generates three integer distributions for each size: seeded random values, ascending values, and descending values. It measures each sorter with `time.perf_counter`, makes a fresh input copy for each repetition, checks the result against Python's `sorted`, and records the median of five runs in CSV. Randomized runs use distinct deterministic seeds for repeatability. The default sizes are 500, 1,000, 2,000, and 4,000.

The included run used Python 3.12.14 on Windows 11 (10.0.26200), seed 2026, and five repetitions. Times are in seconds:

| Input | n | Deterministic | Randomized |
|---|---:|---:|---:|
| Random | 500 | 0.000309 | 0.000418 |
| Random | 1,000 | 0.000566 | 0.000848 |
| Random | 2,000 | 0.004596 | 0.003843 |
| Random | 4,000 | 0.002782 | 0.004055 |
| Sorted | 500 | 0.009733 | 0.001216 |
| Sorted | 1,000 | 0.051912 | 0.002096 |
| Sorted | 2,000 | 0.241735 | 0.004796 |
| Sorted | 4,000 | 0.488184 | 0.003460 |
| Reverse-sorted | 500 | 0.008421 | 0.001228 |
| Reverse-sorted | 1,000 | 0.037316 | 0.002497 |
| Reverse-sorted | 2,000 | 0.085375 | 0.001676 |
| Reverse-sorted | 4,000 | 0.317861 | 0.003767 |

Raw rows are in `benchmark_results.csv`.

### Interpretation

On ascending and descending inputs, the deterministic last-element pivot repeatedly creates an empty partition and a partition containing almost every remaining element. The much longer observed times and their strong increase with input size match the `Θ(n²)` analysis. Random pivoting avoids consistently selecting an extreme rank in these runs and stays in the millisecond range, consistent with expected `Θ(n log n)` behavior.

On random input both versions usually get reasonably balanced pivots. Randomized Quicksort pays for generating random indexes, so it can be slower at small sizes; the measurement confirms that there is no guaranteed constant-factor win on every run. The random-input timings are noisy and not strictly increasing (for example, the 4,000-element deterministic median is below the 2,000-element median). These functions run very quickly at those sizes, so timer resolution, interpreter scheduling, and system activity are a substantial fraction of the measurement. The benchmark is illustrative rather than a precise microbenchmark. Larger sizes, more repetitions, and a quiet machine can improve stability, although deterministic sorted input grows quadratically quickly.

The measurements are consistent with, but do not prove, the asymptotic bounds. They show how pivot selection interacts with specific data, while the recurrence and expected-comparison argument establish the theoretical results.

## 6. Reproduction

From this directory, run:

```bash
python benchmark.py
```

For more repetitions and larger sizes, for example:

```bash
python benchmark.py --sizes 1000 2000 4000 8000 --repeats 9 --seed 2026 --output benchmark_results.csv
```

The program overwrites the selected output CSV and verifies sortedness during every timed batch.
