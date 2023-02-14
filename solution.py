import logging
from typing import List, Optional


def solve_bruteforce(a: List[int], b: List[int]) -> int:
    """Finds the number of multiplicative pairs by comparing each possible pair of indices.

    "Multiplicative" means that for any index 0 <= P < Q < N, C[P] * C[Q] >= C[P] + C[P]
      where C[i] = A[i] + B[i] / 1,000,000
      where A and B are arrays of integers.

    This is a bruteforce solution, iterating over every possible pair.
    The main purpose of it is to serve as a baseline for testing.

    Note: The variables (a, b, c, p, q, n) follow the names from the task description.
    """
    n = len(a)
    c = [aa + bb / 1e6 for aa, bb in zip(a, b)]

    count = 0
    for p in range(n):
        for q in range(p + 1, n):
            if c[p] * c[q] >= c[p] + c[q]:
                count += 1

    return count


def solution(a: List[int], b: List[int]) -> int:
    """Finds a number of multiplicative paris and limits the output by a billion."""
    count = solve_with_boundaries(a, b)
    return min(count, 1_000_000_000)


def solve_with_boundaries(a: List[int], b: List[int]) -> int:
    """Finds number of multiplicative pairs applying some knowledge about the problem.

    Let us explore the problem.
    Here and after, for conciser syntax, mark x = C[P] and y = C[Q].

    By definition, we look for all pairs meeting the criteria `x * y >= x + y`.

    There are 2 scenarios for x:

    1. 0 <= x <= 1

       In this case, the inequality is always met: x * y <= y <= y + x.
       At the same time, by definition, x * y >= x + y.
       That means, for 0 <= x <= 1, the only case that meets criteria is x * y = x + y.

       For non-negative ys, the only good pair is (0, 0).

    2. x > 1

       Let's express y in terms of x, so we can define its boundaries:

         1. x * y >= x + y
         2. x * y - y >= x
         3. y * (x - 1) >= x
         4. y >= x / (x - 1)


       That means, for x = 1.01, y should be at least 101,
                       x = 1.1, y >= 11,
                       x = 1.5, y >= 3 etc.

       Now, by substituting x in the last inequality with 1 + f
       (1 as a whole and f as a fraction == b * 1_000_000), we can simplify the inequetion:
         5. y >= (1 + f) / (1 + f - 1)
         6. y >= (1 + f) / f
         7. y >= 1 + 1 / f
         8. y >= 1 + 1e6 / b


       With this knowledge, we can look for certain values of y.
       Once we discovered the minimal y meeting the requirement,
       all the following pairs (x, y) will meet it as well.


    3. A special case: x >= 2

       For all pairs where x >= 2 and y >= x, x * y will ALWAYS meet criteria.

    4. As the biggest possible number for either y is 1000.999999, the minimal possible x would be

       1.001001 / 0.001001 = 1000.0010

    Summary. We look for:
    ---------------------
      1. all pairs (0, 0)
      2. all pairs with x >= 2
      3. all pairs with 1.001001 <= x < 2 and y >= 1 + 1e6 / b
    """
    last_index = len(a) - 1
    count = 0

    # 1. Find all zeros
    zeros_max_index = find_index(a, b, at_most=0)
    if zeros_max_index is not None:
        count += compute_number_of_combinations(0, zeros_max_index, 1, zeros_max_index)
        logging.info(f"Adding zero counts. Current count is: {count}")

    # 2. Find all numbers greater that or equal two
    at_least_two_min_index = find_index(a, b, at_least=2)
    if at_least_two_min_index is None:
        # If there are no numbers >= 2,
        # it makes no sense to look for solutions, as they don't exist
        logging.warning(f"There are no numbers >= 2. Final count is: {count}")
        return count
    else:
        count += compute_number_of_combinations(
            at_least_two_min_index, last_index, at_least_two_min_index + 1, last_index
        )
        logging.info(
            f"At least two index: {at_least_two_min_index}\tValue:{a[at_least_two_min_index]}.{b[at_least_two_min_index]}"
        )

        logging.info(f"There are numbers >= 2. Current count is: {count}")

    # 3. The intermediate case: 1.001001 <= x < 2, y > 2

    # Iterate over numbers from 1.001001 till 1.999999
    # and try to find their siblings to form multiplier
    # TODO: Use the last element in the array to define initial pointer's location
    left_pointer = find_index(a, b, at_least=1.001001)
    right_pointer = last_index

    while left_pointer < at_least_two_min_index:
        # a[left_pointer] is already 1, so no need to check it
        if b[left_pointer] >= 1001:
            min_y = 1 + 1e6 / b[left_pointer]
            min_y_index = find_index(
                a, b, start_at=left_pointer, finish_at=right_pointer, at_least=min_y
            )
            if min_y_index is not None:
                count += compute_number_of_combinations(
                    left_pointer, at_least_two_min_index - 1, min_y_index, right_pointer
                )
                # Convergence step
                right_pointer = min_y_index - 1

        left_pointer += 1

    logging.info(f"Final count is {count}")

    return count


def compute_number_of_combinations(
    a_from: int, a_to: int, b_from: int, b_to: int
) -> int:
    """Computes a number of permutation pairs without repeats."""
    if a_from > b_from:
        # To simplify the solution, let's order the intervals
        return compute_number_of_combinations(b_from, b_to, a_from, a_to)
    if a_to >= b_to:
        # Exclude equality, 'cause a single element cannot build a pair
        # Any a > b makes no sense, as we expect every pair be ordered
        # All that means, we can shrink the scope of the problem
        return compute_number_of_combinations(a_from, b_to - 1, b_from, b_to)

    a_power = max(a_to - a_from + 1, 0)
    b_power = max(b_to - b_from + 1, 0)

    if a_power == 0 or b_power == 0:
        return 0
    if b_from > a_to:
        return a_power * b_power

    intersection_power = a_to - b_from + 1

    return a_power * b_power - sum(range(intersection_power + 1))


def find_index(
    wholes: List[int],
    fractions: List[int],
    start_at: int = None,
    finish_at: int = None,
    at_least: float = None,
    at_most: float = None,
    default: int = None,
) -> Optional[int]:
    """Finds the minimal index of an element that at least equals the required one.

    If there is no such an element, returns default value.
    """
    assert (
        at_least is not None or at_most is not None
    ), "Parameter `at_least` or `at_most` should been defined!"

    assert not (
        at_least and at_most
    ), "Only one of `at_least`, `at_most` should be defined!"

    assert len(wholes) == len(
        fractions
    ), "`wholes` and `fractions` should be of the same size!"

    start_at = start_at or 0
    finish_at = finish_at if finish_at is not None else len(wholes) - 1

    if start_at >= finish_at:
        return default

    middle = get_middle_index(start_at, finish_at)

    index_found = default
    while start_at <= middle <= finish_at:
        tested_number = wholes[middle] + fractions[middle] / 1_000_000

        if at_least is not None:
            if tested_number >= at_least:
                index_found = middle
                finish_at = middle - 1
            else:
                start_at = middle + 1
        else:
            if tested_number <= at_most:
                index_found = middle
                start_at = middle + 1
            else:
                finish_at = middle - 1

        middle = get_middle_index(start_at, finish_at)

    return index_found


def get_middle_index(start_at, finish_at):
    """For"""
    return start_at + (finish_at - start_at) // 2
