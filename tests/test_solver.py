from __future__ import annotations

import pytest

from sudokulib import solve
from sudokulib.solver import SudokuSolver

GRID_SIZE = 9
BOX_SIZE = 3
MIN_VALUE = 1
MAX_VALUE = 9
EMPTY_CELL = 0
ALL_VALUES = list(range(MIN_VALUE, MAX_VALUE + 1))

test_board = [
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

EXPECTED_SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


class TestSolveFunction:
    """Tests for the public solve() API."""

    def test_solve_returns_correct_solution(self):
        assert solve(test_board) == EXPECTED_SOLUTION

    def test_solve_full_board(self):
        assert solve(EXPECTED_SOLUTION) == EXPECTED_SOLUTION

    def test_solve_invalid_board(self):
        with pytest.raises(ValueError):
            solve([[1, 2], [3, 4]])


class TestSudokuSolver:
    """Tests for the SudokuSolver class."""

    def test_solve_returns_correct_solution(self):
        assert SudokuSolver(test_board).solve() == EXPECTED_SOLUTION

    def test_solve_output_shape(self):
        solution = SudokuSolver(test_board).solve()
        assert len(solution) == GRID_SIZE
        assert all(len(row) == GRID_SIZE for row in solution)

    def test_solve_each_row_has_all_values(self):
        solution = SudokuSolver(test_board).solve()
        assert all(sorted(row) == ALL_VALUES for row in solution)

    def test_solve_each_col_has_all_values(self):
        solution = SudokuSolver(test_board).solve()
        assert all(sorted(solution[r][c] for r in range(GRID_SIZE)) == ALL_VALUES for c in range(GRID_SIZE))

    def test_solve_each_box_has_all_values(self):
        solution = SudokuSolver(test_board).solve()
        for br in range(BOX_SIZE):
            for bc in range(BOX_SIZE):
                box = [solution[br * BOX_SIZE + r][bc * BOX_SIZE + c] for r in range(BOX_SIZE) for c in range(BOX_SIZE)]
                assert sorted(box) == ALL_VALUES

    def test_solve_respects_given_clues(self):
        solution = SudokuSolver(test_board).solve()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if test_board[r][c] != EMPTY_CELL:
                    assert solution[r][c] == test_board[r][c]

    def test_solve_full_board(self):
        solution = SudokuSolver(EXPECTED_SOLUTION).solve()
        assert solution == EXPECTED_SOLUTION

    def test_invalid_board_wrong_dimensions(self):
        with pytest.raises(ValueError):
            SudokuSolver([[1, 2], [3, 4]])

    def test_invalid_board_not_a_list(self):
        with pytest.raises(ValueError):
            SudokuSolver("invalid")

    def test_invalid_cell_value_too_high(self):
        board = [row[:] for row in test_board]
        board[0][0] = MAX_VALUE + 1
        with pytest.raises(ValueError):
            SudokuSolver(board)

    def test_invalid_cell_value_negative(self):
        board = [row[:] for row in test_board]
        board[0][0] = -1
        with pytest.raises(ValueError):
            SudokuSolver(board)

    def test_invalid_cell_non_integer(self):
        board = [row[:] for row in test_board]
        board[0][0] = "5"
        with pytest.raises(ValueError):
            SudokuSolver(board)

    def test_unsolvable_board(self):
        board = [row[:] for row in test_board]
        board[0][0] = 3  # conflicts with board[0][1] = 3
        with pytest.raises(ValueError, match="unsolvable"):
            SudokuSolver(board).solve()
