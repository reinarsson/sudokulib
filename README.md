# sudokulib

A standalone Python library that solves 9×9 Sudoku puzzles using integer linear programming (PuLP/CBC).

## Installation

```bash
pip install -e .
```

## Usage

```python
from sudokulib import solve

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
solution = solve(board)
```

Input: a 9×9 `list[list[int]]` where `0` represents an empty cell and `1`–`9` are given clues.

The `SudokuSolver` class is also available for direct use:

```python
from sudokulib.solver import SudokuSolver

solution = SudokuSolver(board).solve()
```

## Errors

| Exception | When |
|-----------|------|
| `ValueError` | Invalid board dimensions, cell values, or unsolvable puzzle |
| `RuntimeError` | Internal solver failure |

## Tests

```bash
pytest                                              # all tests
pytest -k "test_name"                               # single test
pytest --cov=src/sudokulib --cov-fail-under=80      # with coverage gate
```

## GitHub Actions

The **CI** workflow (`ci.yml`) runs on every push and pull request:

- Tests against Python 3.11 and 3.12
- Enforces 80% coverage threshold
- Lints with flake8
