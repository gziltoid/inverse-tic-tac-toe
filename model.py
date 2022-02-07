#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum


class PlayerMark(Enum):
    X = 1
    O = 2


CellCoords = namedtuple("CellCoords", "row col")


class GameState(Enum):
    IN_PROGRESS = 1
    X_WON = 2
    O_WON = 3
    TIE = 4


class InverseTicTacToeBoard:
    def __init__(self, width, height, losing_length):
        # FIXME check boundaries
        self.__width = width
        self.__height = height
        self.__losing_length = losing_length
        self.__board = [[None] * self.__width for _ in range(self.__height)]
        self.__game_state = GameState.IN_PROGRESS

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def losing_length(self):
        return self.__losing_length

    def is_cell_empty(self, cell):
        return self.__board[cell.row][cell.col] is None

    def __are_there_empty_cells(self):
        return any(None in row for row in self.__board)

    def try_place_marker(self, marker, pos):
        # game is already finished
        if self.__game_state is not GameState.IN_PROGRESS:
            return False
        # trying to place marker out of bounds
        if not (0 <= pos.col < self.__width) or not (0 <= pos.row < self.__height):
            return False
        # cell is not empty
        if not self.is_cell_empty(pos):
            return False

        self.__board[pos.row][pos.col] = marker
        if self.will_lose(marker, pos):
            self.__game_state = (
                GameState.X_WON if marker == PlayerMark.O else GameState.O_WON
            )
        elif not self.__are_there_empty_cells():
            self.__game_state = GameState.TIE
        return True

    def __count_markers(self, marker, pos, delta):
        count = 0
        row, col = pos.row, pos.col
        while True:
            row += delta[0]
            col += delta[1]
            if not (0 <= col < self.__width) or not (0 <= row < self.__height):
                break
            if self.__board[row][col] != marker:
                break
            count += 1
        return count

    def __check_direction(self, marker, pos, delta):
        dx, dy = delta
        count = 1
        # check backward
        count += self.__count_markers(marker, pos, delta=(dx, dy))
        # check forward
        count += self.__count_markers(marker, pos, delta=(-dx, -dy))
        return count >= self.__losing_length

    def will_lose(self, marker, pos):
        return any(
            (
                # check horizontally
                self.__check_direction(marker, pos, delta=(0, -1)),
                # check vertically
                self.__check_direction(marker, pos, delta=(-1, 0)),
                # check main diagonal
                self.__check_direction(marker, pos, delta=(-1, -1)),
                # check antidiagonal
                self.__check_direction(marker, pos, delta=(-1, 1)),
            )
        )

    def get_result(self):
        return self.__game_state


class Bot:
    def __init__(self, board, marker):
        self.__board = board
        self.marker = marker

    def make_a_move(self):
        for row in range(self.__board.height):
            for col in range(self.__board.width):
                cell = CellCoords(row, col)
                if self.__board.is_cell_empty(cell) and not self.__board.will_lose(
                    self.marker, cell
                ):
                    self.__board.try_place_marker(self.marker, cell)
                    return cell
        # place a marker when empty cells are left but player will lose
        for row in range(self.__board.height):
            for col in range(self.__board.width):
                cell = CellCoords(row, col)
                if self.__board.is_cell_empty(cell):
                    self.__board.try_place_marker(self.marker, cell)
                    return cell
        return None


if __name__ == "__main__":
    board = InverseTicTacToeBoard(width=10, height=10, losing_length=5)
    bot = Bot(board, marker=PlayerMark.O)
