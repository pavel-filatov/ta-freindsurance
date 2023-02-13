"""This module contains unit tests for solutions and helper functions."""

from typing import List, Callable, Optional

import pytest

import solution


@pytest.mark.parametrize(
    argnames=["solution_fn"],
    argvalues=[(solution.solve_bruteforce,), (solution.solve_with_boundaries,)],
    ids=["bruteforce", "mathematical approach"],
)
@pytest.mark.parametrize(
    argnames=["a", "b", "expected"],
    argvalues=[
        ([0, 1, 2, 2, 3, 5], [500000, 500000, 0, 0, 0, 20000], 8),
        ([1, 3], [500000, 0], 1),
    ],
    ids=["example-1", "failed-hypothesis"],
)
def test_solutions_minimal_example(
    solution_fn: Callable[[List[int], List[int]], int],
    a: List[int],
    b: List[int],
    expected: int,
):
    assert solution_fn(a, b) == expected


@pytest.mark.parametrize(
    argnames=[
        "wholes",
        "fractions",
        "start_at",
        "finish_at",
        "at_least",
        "at_most",
        "expected_index",
    ],
    argvalues=[
        ([0, 1, 1], [0, 500_000, 700_000], 0, 2, 1.5, None, 1),
        ([0, 1, 1], [0, 500_000, 700_000], 0, 2, 1.51, None, 2),
        ([0, 1, 1], [0, 500_000, 700_000], 0, 2, 1.7, None, 2),
        ([0, 1, 1], [0, 500_000, 700_000], 0, 2, 1.71, None, None),
        ([0, 1, 1, 2], [0, 500_000, 700_000, 0], 0, 3, 1.71, None, 3),
        ([0, 1, 1, 2, 5], [0, 500_000, 700_000, 0, 0], 0, 4, 3, None, 4),
        ([0, 1, 1, 2, 5], [0, 500_000, 700_000, 0, 0], 2, 4, 3, None, 4),
        ([0, 1, 1, 2, 5], [0, 500_000, 700_000, 0, 0], 1, 3, 3, None, None),
        ([0] * 99 + [1], [0] * 100, 0, 99, 1, None, 99),
        ([0] * 99 + [1], [0] * 100, 0, 99, 0, None, 0),
        ([0] * 99 + [1], [0] * 100, 0, 99, 1.000001, None, None),
        # Check at_most works fine
        ([0] * 99 + [1], [0] * 100, 0, 99, None, 0, 98),
        ([0] * 98 + [1], [0] * 99, 0, 99, None, 0, 97),
        # Check our example
        ([0, 1, 2, 2, 3, 5], [500000, 500000, 0, 0, 0, 20000], 0, 5, 2, None, 2),
    ],
)
def test_find_index(
    wholes: List[int],
    fractions: List[int],
    start_at: Optional[int],
    finish_at: Optional[int],
    at_least: Optional[float],
    at_most: Optional[float],
    expected_index: int,
):
    tested_index = solution.find_index(
        wholes, fractions, start_at, finish_at, at_least, at_most
    )

    assert tested_index == expected_index


@pytest.mark.parametrize(
    argnames=["a_from", "a_to", "b_from", "b_to", "expected"],
    argvalues=[
        (0, 4, 1, 4, 10),
        (0, 5, 1, 5, 15),
        (0, 5, 3, 5, 12),
        (1, 4, 10, 13, 16),
        (0, 1, 1, 2, 3),
        (0, 0, 0, 0, 0),
        (0, 0, 0, 1, 1),
        (0, 0, 1, 0, 0),
        (0, 1, 1, 1, 1),
        (2, 5, 3, 5, 6),
        (1, 0, 3, 5, 0),
        # When the intervals are equal
        (10, 13, 10, 13, 6),
    ],
)
def test_compute_number_of_permutations(
    a_from: int, a_to: int, b_from: int, b_to: int, expected: int
):
    assert (
        solution.compute_number_of_combinations(a_from, a_to, b_from, b_to) == expected
    )


@pytest.mark.parametrize(
    argnames=["test_name", "a", "b", "expected"],
    argvalues=[
        ("all zeros", [0] * 100, [0] * 100, sum(range(100))),
        (
            "outputs 1bln when too many pairs",
            [0] * 100_000,
            [0] * 100_000,
            1_000_000_000,
        ),
        ("all ones", [1] * 100_000, [0] * 50_000 + [999_999] * 50_000, 0),
        ("all twos", [2] * 100_000, [0] * 100_000, 1_000_000_000),
        ("all max", [1000] * 100_000, [999_999] * 100_000, 1_000_000_000),
    ],
)
def test_solution_edge_cases(test_name: str, a: List[int], b: List[int], expected: int):
    assert solution.solution(a, b) == expected
