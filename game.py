#!/usr/bin/env python3

PLAYER_MARKS = ['X', 'O']
WIDTH, HEIGHT = 10, 10


class InverseTicTacToe:

    def __init__(self):
        self.board = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def place_marker(self, marker, position):
        pass

    def check_if_player_will_lose(self, marker, position):
        pass

    def get_result(self):
        pass


if __name__ == '__main__':
    game = InverseTicTacToe()
