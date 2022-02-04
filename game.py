#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum


PLAYER_MARKS = ('X', 'O')
WIDTH, HEIGHT = 10, 10
LOSING_LENGTH = 3

Coords = namedtuple('Coords', 'x y')


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
        return self.board[cell.x][cell.y] is None

    def __are_there_empty_cells(self):
        return any(None in row for row in self.board)

    def try_place_marker(self, marker, pos):
        if not self.__is_cell_empty(pos):
            return False
        self.board[pos.x][pos.y] = marker
        if self.check_if_player_will_lose(marker, pos):
            self.game_state = GameState.X_WON if marker == 'O' else GameState.O_WON
        elif not self.__are_there_empty_cells():
            self.game_state = GameState.TIE
        return True

    def check_if_player_will_lose(self, marker, pos):
        count = 1
        # check left
        for cell in self.board[pos.x][pos.y - 1::-1]:
            if cell == marker:
                count += 1
            else:
                break
        # check right
        for cell in self.board[pos.x][pos.y + 1:]:
            if cell == marker:
                count += 1
            else:
                break

        if count == LOSING_LENGTH:
            return True
        else:
            count = 1

        # check above
        for row in self.board[pos.x - 1::-1]:
            if row[pos.y] == marker:
                count += 1
            else:
                break
        # check below
        for row in self.board[pos.x + 1:]:
            if row[pos.y] == marker:
                count += 1
            else:
                break

        if count == LOSING_LENGTH:
            return True
        else:
            count = 1

        # check left diagonal upward
        col = pos.y
        for row in self.board[pos.x - 1::-1]:
            col -= 1
            if row[col] == marker:
                count += 1
            else:
                break
        # check left diagonal downward
        col = pos.y
        for row in self.board[pos.x + 1:]:
            col += 1
            if row[col] == marker:
                count += 1
            else:
                break

        if count == LOSING_LENGTH:
            return True
        else:
            count = 1

        # check right diagonal upward
        col = pos.y
        for row in self.board[pos.x - 1::-1]:
            col += 1
            if row[col] == marker:
                count += 1
            else:
                break
        # check right diagonal downward
        col = pos.y
        for row in self.board[pos.x + 1:]:
            col -= 1
            if row[col] == marker:
                count += 1
            else:
                break

        if count == LOSING_LENGTH:
            return True
        else:
            count = 1

        return False

    def get_result(self):
        return self.game_state


if __name__ == '__main__':
    game = InverseTicTacToeBoard(WIDTH, HEIGHT)
