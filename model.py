from enum import Enum
from typing import Optional
from typing import NamedTuple
from typing import Optional


class PlayerMark(Enum):
    X = 1
    O = 2


class CellCoords(NamedTuple):
    row: int
    col: int


class GameState(Enum):
    IN_PROGRESS = 1
    X_WON = 2
    O_WON = 3
    TIE = 4


class InverseTicTacToeBoard:
    def __init__(self, row_count: int, col_count: int, losing_length: int):
        if row_count <= 0 or col_count <= 0:
            raise ValueError("Width and row_count should be positive.")
        if losing_length <= 0 or losing_length > col_count or losing_length > row_count:
            raise ValueError(
                "Losing length should be positive and less than col_count or row_count."
            )
        self.__col_count = col_count
        self.__row_count = row_count
        self.__losing_length = losing_length
        self.__board = [
            [None] * self.__col_count for _ in range(self.__row_count)]
        self.__game_state = GameState.IN_PROGRESS

    @property
    def col_count(self) -> int:
        return self.__col_count

    @property
    def row_count(self) -> int:
        return self.__row_count

    @property
    def losing_length(self) -> int:
        return self.__losing_length

    def is_cell_empty(self, cell: CellCoords) -> bool:
        return self.__board[cell.row][cell.col] is None

    def __are_empty_cells_left(self) -> bool:
        return any(None in row for row in self.__board)

    def try_place_marker(self, marker: PlayerMark, cell: CellCoords) -> bool:
        # game is already finished
        if self.__game_state is not GameState.IN_PROGRESS:
            return False
        # trying to place marker out of bounds
        if not (0 <= cell.row < self.__row_count) or not (
            0 <= cell.col < self.__col_count
        ):
            return False
        # cell is not empty
        if not self.is_cell_empty(cell):
            return False

        self.__board[cell.row][cell.col] = marker
        if self.will_lose(marker, cell):
            self.__game_state = (
                GameState.X_WON if marker == PlayerMark.O else GameState.O_WON
            )
        elif not self.__are_empty_cells_left():
            self.__game_state = GameState.TIE
        return True

    def __count_markers(
        self, marker: PlayerMark, starting_cell: CellCoords, delta: tuple[int, int]
    ) -> int:
        row, col = starting_cell.row, starting_cell.col
        count = 0
        dx, dy = delta
        while True:
            row += dx
            col += dy
            if not (0 <= row < self.__row_count) or not (0 <= col < self.__col_count):
                break
            if self.__board[row][col] != marker:
                break
            count += 1
        return count

    def __check_direction(
        self, marker: PlayerMark, starting_cell: CellCoords, delta: tuple[int, int]
    ) -> bool:
        count = 1  # starting_cell is counted
        dx, dy = delta
        # check backward
        count += self.__count_markers(marker, starting_cell, delta=(dx, dy))
        # check forward
        count += self.__count_markers(marker, starting_cell, delta=(-dx, -dy))
        return count >= self.__losing_length

    def will_lose(self, marker: PlayerMark, cell: CellCoords) -> bool:
        return any(
            (
                # check horizontally
                self.__check_direction(marker, cell, delta=(0, -1)),
                # check vertically
                self.__check_direction(marker, cell, delta=(-1, 0)),
                # check main diagonal
                self.__check_direction(marker, cell, delta=(-1, -1)),
                # check antidiagonal
                self.__check_direction(marker, cell, delta=(-1, 1)),
            )
        )

    def get_result(self) -> GameState:
        return self.__game_state


class Bot:
    def __init__(self, board: list[list[Optional[PlayerMark]]], marker: PlayerMark):
        self.__board = board
        self.marker = marker

    def make_a_move(self) -> Optional[CellCoords]:
        for row in range(self.__board.row_count):
            for col in range(self.__board.col_count):
                cell = CellCoords(row, col)
                if self.__board.is_cell_empty(cell) and not self.__board.will_lose(
                    self.marker, cell
                ):
                    self.__board.try_place_marker(self.marker, cell)
                    return cell
        # place a marker when empty cells are left but player will lose
        for row in range(self.__board.row_count):
            for col in range(self.__board.col_count):
                cell = CellCoords(row, col)
                if self.__board.is_cell_empty(cell):
                    self.__board.try_place_marker(self.marker, cell)
                    return cell
        return None
