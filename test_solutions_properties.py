"""This module contains properties tests.

The main ideas here are:
  1. to compare an optimized solution against the bruteforce (that surely produces right results)
     for arbitrary inputs
  2. compare both solutions against the common edge cases with arbitrary inputs
"""

from typing import Tuple, List, Callable

import pytest
from hypothesis import strategies as st, settings, given

import solution


def generate_arrays_of_wholes_and_fractions(
    min_size: int = 0,
    min_whole: int = 0,
    max_whole: int = 1000,
    min_fraction: int = 0,
    max_fraction: int = 999_999,
) -> st.SearchStrategy[Tuple[List[int], List[int]]]:
    """Generates a tuple of lists emulating arrays A and B."""
    # Generator for a single tuple (whole, fraction)
    gen_whole_fraction = st.tuples(
        st.integers(min_value=min_whole, max_value=max_whole),
        st.integers(min_value=min_fraction, max_value=max_fraction),
    )

    return (
        st.lists(gen_whole_fraction, min_size=min_size, max_size=100_000)
        .map(sorted)
        .map(lambda ab: ([a for a, _ in ab], [b for _, b in ab]))
    )


@settings(print_blob=True)
@given(generate_arrays_of_wholes_and_fractions())
def test_compare_solution_with_bruteforce_variant__small_examples(
    ab: Tuple[List[int], List[int]]
):
    """Checks the equality between outputs from the bruteforce solution and the solution with bounds
    for arbitrary inputs."""
    a, b = ab

    assert solution.solve_with_boundaries(a, b) == solution.solve_bruteforce(a, b), ab


@settings(print_blob=True)
@given(generate_arrays_of_wholes_and_fractions(min_size=200))
def test_compare_solution_with_bruteforce_variant__bigger_examples(
    ab: Tuple[List[int], List[int]]
):
    """Checks the equality between outputs from the bruteforce solution and the solution with bounds
    for arbitrary inputs.

    This case covers bigger input arrays.
    """
    a, b = ab

    assert solution.solve_with_boundaries(a, b) == solution.solve_bruteforce(a, b), ab


@pytest.mark.parametrize(
    argnames=["solution_fn"],
    argvalues=[(solution.solve_bruteforce,), (solution.solve_with_boundaries,)],
    ids=["bruteforce", "mathematical approach"],
)
@settings(print_blob=True)
@given(
    generate_arrays_of_wholes_and_fractions(
        min_size=200, min_whole=0, min_fraction=1, max_whole=1
    )
)
def test_compare_solution_with_bruteforce_variant__small_numbers_only(
    solution_fn: Callable[[List[int], List[int]], int],
    ab: Tuple[List[int], List[int]],
):
    """Checks that there are no multiplicative pairs if all numbers are small."""
    a, b = ab

    assert solution_fn(a, b) == 0
