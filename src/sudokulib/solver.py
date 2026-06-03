from __future__ import annotations

import pulp

GRID_SIZE = 9
BOX_SIZE = 3
MIN_VALUE = 1
MAX_VALUE = 9
EMPTY_CELL = 0


class SudokuSolver:
    """Solve a 9x9 Sudoku puzzle using integer linear programming (PuLP/CBC)."""

    def __init__(self, board: list[list[int]]) -> None:
        self._validate(board)
        self.board = board

    def _validate(self, board: list[list[int]]) -> None:
        if not isinstance(board, list) or len(board) != GRID_SIZE:
            raise ValueError(f"Board must be a {GRID_SIZE}x{GRID_SIZE} list")
        for r, row in enumerate(board):
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                raise ValueError(f"Row {r} must be a list of {GRID_SIZE} integers")
            for c, val in enumerate(row):
                if not isinstance(val, int) or not (EMPTY_CELL <= val <= MAX_VALUE):
                    raise ValueError(f"Cell ({r},{c}) must be an integer between 0 and {MAX_VALUE}, got {val!r}")

    def solve(self) -> list[list[int]]:
        """Solve the puzzle and return the completed 9x9 grid."""
        rows = cols = range(GRID_SIZE)
        boxes = [(r, c) for r in range(BOX_SIZE) for c in range(BOX_SIZE)]
        values = range(MIN_VALUE, MAX_VALUE + 1)

        try:
            prob = pulp.LpProblem("sudoku", pulp.LpMinimize)
            x = pulp.LpVariable.dicts("x", (rows, cols, values), cat="Binary")

            for r in rows:
                for c in cols:
                    prob += pulp.lpSum(x[r][c][v] for v in values) == 1

            for r in rows:
                for v in values:
                    prob += pulp.lpSum(x[r][c][v] for c in cols) == 1

            for c in cols:
                for v in values:
                    prob += pulp.lpSum(x[r][c][v] for r in rows) == 1

            for br, bc in boxes:
                for v in values:
                    prob += pulp.lpSum(
                        x[br * BOX_SIZE + r][bc * BOX_SIZE + c][v]
                        for r in range(BOX_SIZE) for c in range(BOX_SIZE)
                    ) == 1

            for r in rows:
                for c in cols:
                    if self.board[r][c] != EMPTY_CELL:
                        prob += x[r][c][self.board[r][c]] == 1

            prob.solve(pulp.PULP_CBC_CMD(msg=0))
        except pulp.PulpSolverError as e:
            raise RuntimeError(f"Solver failed: {e}") from e

        if pulp.LpStatus[prob.status] != "Optimal":
            raise ValueError("Sudoku puzzle is unsolvable")

        return [self._extract_row(x, r, cols, values) for r in rows]

    def _extract_row(self, x: dict, r: int, cols: range, values: range) -> list[int]:
        row = [int(v) for c in cols for v in values if pulp.value(x[r][c][v]) == 1]
        if len(row) != GRID_SIZE:
            raise RuntimeError(f"Solver produced invalid output for row {r}: expected {GRID_SIZE} values, got {len(row)}")
        return row
