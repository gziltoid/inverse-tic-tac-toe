#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum


PLAYER_MARKS = ['X', 'O']
WIDTH, HEIGHT = 10, 10
LOOSING_LENGTH = 5

Coords = namedtuple('Coords', 'x y')


class GameState(Enum):
    IN_PROGRESS = 1
    X_WON = 2
    O_WON = 3
    TIE = 4


class InverseTicTacToeBoard:

    def __init__(self):
        self.board = [[None] * WIDTH for _ in range(HEIGHT)]
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

        if count == LOOSING_LENGTH:
            return True
        else:
            count = 1

        # check above
        for cell in self.board[pos.x - 1::-1][pos.y]:
            if cell == marker:
                count += 1
            else:
                break
        # check below
        for cell in self.board[pos.x + 1:][pos.y]:
            if cell == marker:
                count += 1
            else:
                break

        if count == LOOSING_LENGTH:
            return True
        else:
            count = 1

        # check left diagonal upward
        for cell in self.board[pos.x - 1::-1][pos.y - 1::-1]:
            if cell == marker:
                count += 1
            else:
                break
        # check left diagonal downward
        for cell in self.board[pos.x + 1:][pos.y + 1:]:
            if cell == marker:
                count += 1
            else:
                break

        # check right diagonal upward
        for cell in self.board[pos.x - 1::-1][pos.y + 1:]:
            if cell == marker:
                count += 1
            else:
                break
        # check right diagonal downward
        for cell in self.board[pos.x + 1:][pos.y - 1::-1]:
            if cell == marker:
                count += 1
            else:
                break

        if count == LOOSING_LENGTH:
            return True
        else:
            count = 1

        return False

    def get_result(self):
        return self.game_state


if __name__ == '__main__':
    game = InverseTicTacToeBoard()
