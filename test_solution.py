import pytest

import solution


@pytest.mark.parametrize(
    argnames=["solution_fn"], argvalues=[(solution.bruteforce_solution, )]
)
def test_solutions_minimal_example(solution_fn: solution.Solution):
    a = [0, 1, 2, 2, 3, 5]
    b = [500000, 500000, 0, 0, 0, 20000]

    assert solution_fn(a, b) == 8
