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

1. **Always start from the latest `main`:**
   ```bash
   git checkout main && git pull origin main
   ```
2. **Never commit directly to `main`.** Always create a feature branch from it:
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. Do all work on that branch and commit changes there.
4. Before opening a PR, run `pytest --cov=src/sudokulib --cov-fail-under=80`. Do not open a PR if coverage is below 80%.
5. Open a PR to merge into `main` using `gh pr create`.
6. After opening the PR, monitor its status with `gh pr checks`. If any checks fail or review comments are posted, fix the issues on the same branch, commit, and push. Repeat until all checks pass and comments are resolved.

## Architecture

A standalone Python package (`sudokulib`) that exposes a single class:

- `SudokuSolver(board)` — validates and solves a 9×9 Sudoku using integer linear programming (PuLP/CBC)
- Input: 9×9 `list[list[int]]` where `0` = empty cell
- Output: solved 9×9 `list[list[int]]`
- Raises `ValueError` for invalid boards or unsolvable puzzles; `RuntimeError` for solver failures

Installed as an editable package (`pip install -e .`) and consumed by `sudokuservice` as a dependency. When making changes here, re-install or verify `sudokuservice` tests still pass.

## Code Standards

- No magic numbers or strings — define a named constant and use that instead
- **Python 3.11+**, `from __future__ import annotations` in every file
- Type hints on all signatures; Google-style docstrings on all public methods
- Branch naming: `feat/`, `fix/`, `chore/`, `refactor/`, `test/`; Conventional Commits format
