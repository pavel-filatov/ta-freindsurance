# ta-friendsurance

Test assignment for Friendsurance.

## Prerequisites

- Python 3.7+
- Docker

## How to run

### Set up SQL Server

To solve and test the SQL-related tasks, the Docker stack is used.
To set it up and running, use a simple compose command:

```shell
docker compose up
```

Check [`docker-compose.yml`](./docker-compose.yml) to learn more.

## Task 2: Python Challenge

The goal of the task is to find a number of multiplicative pairs.

The task description and reasoning behind the solution are presented in
the [corresponding docs](./docs/02_find_multiplicative_pairs.md).

The solution itself is implemented as a Python function named `solution()`
in the [`solution.py` file](./solution.py).

### How to run

As soon as solution is a plain Python function, and there are no requirements
for interaction with the outer world, it's not runnable as a standalone application.

But this project contains a number of tests:

- [`test_solution.py`](./test_solution.py) is dedicated for fast unit tests
- [`test_solutions_properties.py`](./test_solutions_properties.py) is for
  slow property-based tests (it checks how any solution complies with general laws)

To run tests, use Poetry dependencies manager:

```shell
poetry install && poetry run pytest
```

Poetry will install all dependencies needed to test the app and
run all Pytest suites.

Poetry is chosen because it allows easily manage virtual environments.
Learn more at the website: https://python-poetry.org.

## Improvement ideas

- Optimizations for the Python task:
    - Set the left pointer by finding the biggest element and computing the least
      value meeting the criteria
    - Keep track of the last processed value of the left pointer
    - Simplify `compute_number_of_combinations`
- Create an architecture for the task 3
- Experiment with Pivot SQL queries; is it efficient enough or require filtering beforehand?
