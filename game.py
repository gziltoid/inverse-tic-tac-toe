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


class InverseTicTacToeBoard(object):
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

    def __is_cell_empty(self, cell):
        return self.__board[cell.row][cell.col] is None

    def __are_there_empty_cells(self):
        return any(None in row for row in self.__board)

    def try_place_marker(self, marker, pos):
        if not (0 <= pos.row < self.__width) or not (0 <= pos.col < self.__height):
            return False
        if not self.__is_cell_empty(pos):
            return False
        self.__board[pos.row][pos.col] = marker
        if self.check_if_player_will_lose(marker, pos):
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
        return count == self.__losing_length

    def check_if_player_will_lose(self, marker, pos):
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


if __name__ == "__main__":
    game = InverseTicTacToeBoard(width=10, height=10, losing_length=5)
