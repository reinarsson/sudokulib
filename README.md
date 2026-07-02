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

## PuLP MIP model

Indices: $r$ = row, $c$ = column, $v$ = digit value (all ranging over $\{1,\ldots,9\}$).

Decision variable: $x_{r,c,v} \in \{0,1\}$ — equals 1 if cell $(r,c)$ contains digit $v$, otherwise 0.

**1. Each cell holds exactly one digit:**
$$\Large \sum_{v=1}^{9} x_{r,c,v} = 1 \qquad \forall\; r,c \in \{1,\ldots,9\}$$

**2. Each digit appears exactly once per row:**
$$\Large \sum_{c=1}^{9} x_{r,c,v} = 1 \qquad \forall\; r,v \in \{1,\ldots,9\}$$

**3. Each digit appears exactly once per column:**
$$\Large \sum_{r=1}^{9} x_{r,c,v} = 1 \qquad \forall\; c,v \in \{1,\ldots,9\}$$

**4. Each digit appears exactly once per 3×3 box:**
$$\Large \sum_{i=0}^{2}\sum_{j=0}^{2} x_{b_r+i,\; b_c+j,\; v} = 1 \qquad \forall\; b_r,b_c \in \{0,3,6\},\; v \in \{1,\ldots,9\}$$

**5. Pre-filled clues are fixed:**
$$\Large x_{r,c,\,g_{r,c}} = 1 \qquad \forall\; (r,c) \text{ where } g_{r,c} \neq 0$$

where $g_{r,c}$ is the given digit at cell $(r,c)$.