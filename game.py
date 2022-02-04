#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum

# FIXME: move to class ?
PLAYER_MARKS = ('X', 'O')
WIDTH, HEIGHT = 10, 10
LOSING_LENGTH = 5

CellCoords = namedtuple('CellCoords', 'row col')


class GameState(Enum):
    IN_PROGRESS = 1
    X_WON = 2
    O_WON = 3
    TIE = 4


class InverseTicTacToeBoard:

    def __init__(self, width, height):
        self.board = [[None] * width for _ in range(height)]
        self.game_state = GameState.IN_PROGRESS

    def __is_cell_empty(self, cell):
        return self.board[cell.row][cell.] is None

    def __are_there_empty_cells(self):
        return any(None in row for row in self.board)

    def try_place_marker(self, marker, pos):
        if not (0 <= pos.row < WIDTH) or not (0 <= pos.col < HEIGHT):
            return False
        if not self.__is_cell_empty(pos):
            return False
        self.board[pos.row][pos.col] = marker
        if self.check_if_player_will_lose(marker, pos):
            self.game_state = GameState.X_WON if marker == 'O' else GameState.O_WON
        elif not self.__are_there_empty_cells():
            self.game_state = GameState.TIE
        return True

    def check_if_player_will_lose(self, marker, pos):
        count = 1
        # check left
        row, col = pos.row, pos.col
        if col > 0:
            for cell in self.board[row][col - 1::-1]:
                if cell == marker:
                    count += 1
                    if count == LOSING_LENGTH:
                        return True
                else:
                    break
        # check right
        row, col = pos.row, pos.col
        if col < WIDTH - 1:
            for cell in self.board[row][col + 1:]:
                if cell == marker:
                    count += 1
                    if count == LOSING_LENGTH:
                        return True
                else:
                    break

        count = 1
        # check above
        row, col = pos.row, pos.col
        if row > 0:
            for arr in self.board[row - 1::-1]:
                if arr[col] == marker:
                    count += 1
                    if count == LOSING_LENGTH:
                        return True
                else:
                    break
        # check below
        row, col = pos.row, pos.col
        if row < HEIGHT - 1:
            for arr in self.board[row + 1:]:
                if arr[col] == marker:
                    count += 1
                    if count == LOSING_LENGTH:
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
            if self.board[row][col] != marker:
                break
            count += 1
            if count == LOSING_LENGTH:
                return True
        # check main diagonal downward
        row, col = pos.row, pos.col
        while True:
            row += 1
            col += 1
            if row > HEIGHT - 1 or col > WIDTH - 1:
                break
            if self.board[row][col] != marker:
                break
            count += 1
            if count == LOSING_LENGTH:
                return True

        count = 1
        # check antidiagonal upward
        row, col = pos.row, pos.col
        while True:
            row -= 1
            col += 1
            if row < 0 or col > WIDTH - 1:
                break
            if self.board[row][col] != marker:
                break
            count += 1
            if count == LOSING_LENGTH:
                return True
        # check antidiagonal downward
        row, col = pos.row, pos.col
        while True:
            row += 1
            col -= 1
            if row > HEIGHT - 1 or col < 0:
                break
            if self.board[row][col] != marker:
                break
            count += 1
            if count == LOSING_LENGTH:
                return True

        return False

    def get_result(self):
        return self.game_state


if __name__ == '__main__':
    game = InverseTicTacToeBoard(WIDTH, HEIGHT)
