# ta-friendsurance

Test assignment for Friendsurance.

## Prerequisites

- Python 3.7+
- Poetry
- Docker

## Task 1: Create SQL Queries

### Preparations

#### Set up SQL Server

To solve and test the SQL-related tasks, the Docker stack is used.
To set it up and running, use a simple compose command:

```shell
docker compose up
```

Check [`docker-compose.yml`](./docker-compose.yml) to learn more.

All the SQL scripts are mounted from the `./sql` local directory to the `/sql` directory inside a container.

:exclamation: Don't forget to teardown once the job is done:

```shell
docker compose down
```

#### Initialize the database

To initialize the database and make it possible to run examples, execute the command:

```shell
docker exec -it friendsurance-sql-server-1 bash /scripts/run-sql.sh init-db
```

Once the script is done, you're free to go with examples.

### Run the examples

Running the queries is done the same way as DB initialization.
The only difference there is the command choose `task-1` instead of the `init-db`
to run the SQL script for the 1st task, `task-2` for the second etc.
Example:

```shell
docker exec friendsurance-sql-server-1 bash /scripts/run-sql.sh [task-1,task-2,task-3]
```

**Note:** some tasks may have adjustable parameters, please check the corresponding scripts to find out more.

The results of the tasks are written into the `./output` directory.

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

- Create an architecture for the task 3
- Experiment with Pivot SQL queries; is it efficient enough or require filtering beforehand?
