"""In-place deterministic and randomized Quicksort implementations."""

from random import Random
from typing import MutableSequence, Optional, TypeVar

T = TypeVar("T")


def quicksort(values: MutableSequence[T]) -> MutableSequence[T]:
    """Sort *values* in place using the last element as each pivot.

    Lomuto partitioning makes this implementation easy to follow. Equal keys
    go to the left partition, which means duplicate-heavy inputs can expose
    its quadratic behavior. Returns the same sequence for convenient use.
    """
    def partition(lo: int, hi: int) -> int:
        pivot = values[hi]
        boundary = lo
        for scan in range(lo, hi):
            if values[scan] <= pivot:
                values[boundary], values[scan] = values[scan], values[boundary]
                boundary += 1
        values[boundary], values[hi] = values[hi], values[boundary]
        return boundary

    def sort(lo: int, hi: int) -> None:
        # Recurse on the smaller side and iterate over the larger side. This
        # preserves Quicksort's comparisons while bounding Python stack depth.
        while lo < hi:
            pivot_index = partition(lo, hi)
            if pivot_index - lo < hi - pivot_index:
                sort(lo, pivot_index - 1)
                lo = pivot_index + 1
            else:
                sort(pivot_index + 1, hi)
                hi = pivot_index - 1

    sort(0, len(values) - 1)
    return values


def randomized_quicksort(
    values: MutableSequence[T], *, seed: Optional[int] = None
) -> MutableSequence[T]:
    """Sort *values* in place, choosing a uniformly random pivot per range.

    Supplying *seed* makes runs reproducible. The input is still mutated and
    the same sequence is returned.
    """
    rng = Random(seed)

    def partition(lo: int, hi: int) -> int:
        pivot_index = rng.randint(lo, hi)
        values[pivot_index], values[hi] = values[hi], values[pivot_index]
        pivot = values[hi]
        boundary = lo
        for scan in range(lo, hi):
            if values[scan] <= pivot:
                values[boundary], values[scan] = values[scan], values[boundary]
                boundary += 1
        values[boundary], values[hi] = values[hi], values[boundary]
        return boundary

    def sort(lo: int, hi: int) -> None:
        while lo < hi:
            pivot_index = partition(lo, hi)
            if pivot_index - lo < hi - pivot_index:
                sort(lo, pivot_index - 1)
                lo = pivot_index + 1
            else:
                sort(pivot_index + 1, hi)
                hi = pivot_index - 1

    sort(0, len(values) - 1)
    return values
