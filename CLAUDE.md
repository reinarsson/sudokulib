# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run tests**
```bash
pytest
```

**Run a single test**
```bash
pytest -k "test_name"
```

**Run with coverage**
```bash
pytest --cov=src/sudokulib --cov-fail-under=80
```

**Install as editable package (required by sudokuservice)**
```bash
pip install -e .
```

## Git workflow — mandatory for all agents

1. **Never commit directly to `main`.** Always start by creating a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Do all work on that branch and commit changes there.
3. Before opening a PR, run `pytest --cov=src/sudokulib --cov-fail-under=80`. Do not open a PR if coverage is below 80%.
4. Open a PR to merge into `main` using `gh pr create`.

## Architecture

A standalone Python package (`sudokulib`) that exposes a single class:

- `SudokuSolver(board)` — validates and solves a 9×9 Sudoku using integer linear programming (PuLP/CBC)
- Input: 9×9 `list[list[int]]` where `0` = empty cell
- Output: solved 9×9 `list[list[int]]`
- Raises `ValueError` for invalid boards or unsolvable puzzles; `RuntimeError` for solver failures

Installed as an editable package (`pip install -e .`) and consumed by `sudokuservice` as a dependency. When making changes here, re-install or verify `sudokuservice` tests still pass.

## Code Standards

- **Python 3.11+**, `from __future__ import annotations` in every file
- Type hints on all signatures; Google-style docstrings on all public methods
- Branch naming: `feat/`, `fix/`, `chore/`, `refactor/`; Conventional Commits format
