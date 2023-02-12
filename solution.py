from typing import List, Callable

Solution = Callable[[List[int], List[int]], int]


def bruteforce_solution(a: List[int], b: List[int]) -> int:
    """Compares each possible pair of indices."""
    count = 0

    c = [aa + bb / 1e6 for aa, bb in zip(a, b)]

    for idx in range(len(c)):
        for idy in range(len(c)):
            if idx < idy and c[idx] * c[idy] >= c[idx] + c[idy]:
                count += 1

    return count
