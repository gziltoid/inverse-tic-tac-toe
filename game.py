#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum

# FIXME: enum?
PLAYER_MARKS = ('X', 'O')

CellCoords = namedtuple('CellCoords', 'row col')


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
        self.__board = [[None] * self.width for _ in range(self.height)]
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
        if not (0 <= pos.row < self.width) or not (0 <= pos.col < self.height):
            return False
        if not self.__is_cell_empty(pos):
            return False
        self.__board[pos.row][pos.col] = marker
        if self.check_if_player_will_lose(marker, pos):
            self.__game_state = GameState.X_WON if marker == 'O' else GameState.O_WON
        elif not self.__are_there_empty_cells():
            self.__game_state = GameState.TIE
        return True

    def check_if_player_will_lose(self, marker, pos):
        count = 1
        # check left
        row, col = pos.row, pos.col
        if col > 0:
            for cell in self.__board[row][col - 1::-1]:
                if cell == marker:
                    count += 1
                    if count == self.losing_length:
                        return True
                else:
                    break
        # check right
        row, col = pos.row, pos.col
        if col < self.width - 1:
            for cell in self.__board[row][col + 1:]:
                if cell == marker:
                    count += 1
                    if count == self.losing_length:
                        return True
                else:
                    break

        count = 1
        # check above
        row, col = pos.row, pos.col
        if row > 0:
            for arr in self.__board[row - 1::-1]:
                if arr[col] == marker:
                    count += 1
                    if count == self.losing_length:
                        return True
                else:
                    break
        # check below
        row, col = pos.row, pos.col
        if row < self.height - 1:
            for arr in self.__board[row + 1:]:
                if arr[col] == marker:
                    count += 1
                    if count == self.losing_length:
                        return True
                else:
                    break

        count = 1
        # check main diagonal upward
        row, col = pos.row, pos.col
        while True:
            row -= 1
            col -= 1
            if row < 0 or col < 0:
                break
            if self.__board[row][col] != marker:
                break
            count += 1
            if count == self.losing_length:
                return True
        # check main diagonal downward
        row, col = pos.row, pos.col
        while True:
            row += 1
            col += 1
            if row > self.height - 1 or col > self.width - 1:
                break
            if self.__board[row][col] != marker:
                break
            count += 1
            if count == self.losing_length:
                return True

        count = 1
        # check antidiagonal upward
        row, col = pos.row, pos.col
        while True:
            row -= 1
            col += 1
            if row < 0 or col > self.width - 1:
                break
            if self.__board[row][col] != marker:
                break
            count += 1
            if count == self.losing_length:
                return True
        # check antidiagonal downward
        row, col = pos.row, pos.col
        while True:
            row += 1
            col -= 1
            if row > self.height - 1 or col < 0:
                break
            if self.__board[row][col] != marker:
                break
            count += 1
            if count == self.losing_length:
                return True

        return False

    def get_result(self):
        return self.__game_state


if __name__ == '__main__':
    game = InverseTicTacToeBoard(width=10, height=10, losing_length=5)
