# Design Document — sudokulib

## Overview

`sudokulib` is a framework-agnostic Python library that solves 9×9 Sudoku puzzles using integer linear programming. It has no dependency on FastAPI, Dash, or any web framework and can be used in any Python application.

---

## Patterns

### 1. Encapsulation via a Single Public Class

All solving logic is encapsulated in `SudokuSolver`. Input validation, LP model construction, solving, and result extraction are private methods. The caller only interacts with two things:

```python
solver = SudokuSolver(board)   # validates on construction
solution = solver.solve()      # raises on unsolvable or solver error
```

Validation at construction time means a bad board fails immediately, before any expensive LP work begins.

### 2. Named Constants Over Magic Numbers

All grid dimensions are defined as module-level constants (`GRID_SIZE`, `BOX_SIZE`, `MIN_VALUE`, `MAX_VALUE`, `EMPTY_CELL`) and used throughout. This makes the code self-documenting and means changing to a 16×16 variant requires only constant updates.

### 3. Flat Public API

The package exposes a `solve(board)` convenience function from `__init__.py`, wrapping `SudokuSolver` for callers that don't need direct class access:

```python
import sudokulib
solution = sudokulib.solve(board)
```

---

## Solving Approach

The puzzle is modelled as a **binary integer linear program**:

- A binary variable `x[r][c][v]` = 1 if cell `(r, c)` holds value `v`, 0 otherwise
- Constraints enforce that each cell has exactly one value, each value appears once per row, once per column, and once per 3×3 box
- Given clues fix the corresponding variables to 1
- The CBC solver (bundled with PuLP) finds a feasible solution

There is no objective function to optimise — the problem is pure feasibility. `LpMinimize` is set as the sense as required by PuLP's API, but no objective is added.

---

## Error Handling

| Situation | Exception |
|-----------|-----------|
| Invalid board dimensions or values | `ValueError` (raised in `__init__`) |
| Unsolvable puzzle | `ValueError` (raised after solve) |
| CBC solver internal failure | `RuntimeError` (wraps `PulpSolverError`) |
| Solver returns wrong number of values per row | `RuntimeError` (raised in `_extract_row`) |
