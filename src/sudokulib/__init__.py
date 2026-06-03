"""Sudoku solving library."""

from __future__ import annotations

from sudokulib.solver import SudokuSolver

__all__ = ["solve"]


def solve(board: list[list[int]]) -> list[list[int]]:
    """Solve a 9x9 Sudoku puzzle and return the completed grid.

    Args:
        board: A 9x9 grid where 0 represents empty cells and 1-9 are given clues.

    Returns:
        The solved 9x9 grid.

    Raises:
        ValueError: If the board is invalid or unsolvable.
        RuntimeError: If the solver encounters an internal error.
    """
    return SudokuSolver(board).solve()
