from game import InverseTicTacToeBoard, PLAYER_MARKS, CellCoords, GameState
from pprint import pprint
import pytest


@pytest.fixture(autouse=True)
def game():
    game = InverseTicTacToeBoard(width=10, height=10, losing_length=5)
    yield game


def test_placing_markers(game):
    x = PLAYER_MARKS[0]
    o = PLAYER_MARKS[1]
    game.try_place_marker(x, CellCoords(1, 1))
    game.try_place_marker(o, CellCoords(2, 2))
    assert game._InverseTicTacToeBoard__board[1][1] == 'X'
    assert game._InverseTicTacToeBoard__board[2][2] == 'O'
    assert game.get_result() is GameState.IN_PROGRESS
    # can't place a marker when cell is not empty
    assert game.try_place_marker(x, CellCoords(1, 1)) is False
    assert game.try_place_marker(o, CellCoords(2, 2)) is False
    # bounds check
    assert game.try_place_marker(x, CellCoords(-1, -1)) is False
    assert game.try_place_marker(x, CellCoords(0, 0)) is True
    assert game.try_place_marker(x, CellCoords(-1, 10)) is False
    assert game.try_place_marker(x, CellCoords(0, 9)) is True
    assert game.try_place_marker(x, CellCoords(10, -1)) is False
    assert game.try_place_marker(x, CellCoords(9, 0)) is True
    assert game.try_place_marker(x, CellCoords(10, 10)) is False
    assert game.try_place_marker(x, CellCoords(9, 9)) is True
    # pprint(game.board)


def test_check_horizontal_losing(game):
    x = PLAYER_MARKS[0]
    game.try_place_marker(x, CellCoords(1, 1))
    game.try_place_marker(x, CellCoords(1, 2))
    game.try_place_marker(x, CellCoords(1, 5))
    game.try_place_marker(x, CellCoords(1, 4))
    game.try_place_marker(x, CellCoords(1, 3))
    assert game.get_result() is GameState.O_WON


def test_check_vertical_losing(game):
    o = PLAYER_MARKS[1]
    game.try_place_marker(o, CellCoords(2, 4))
    game.try_place_marker(o, CellCoords(3, 4))
    game.try_place_marker(o, CellCoords(6, 4))
    game.try_place_marker(o, CellCoords(5, 4))
    game.try_place_marker(o, CellCoords(4, 4))
    assert game.get_result() is GameState.X_WON


def test_check_main_diagonal_losing(game):
    x = PLAYER_MARKS[0]
    game.try_place_marker(x, CellCoords(1, 1))
    game.try_place_marker(x, CellCoords(2, 2))
    game.try_place_marker(x, CellCoords(5, 5))
    game.try_place_marker(x, CellCoords(4, 4))
    game.try_place_marker(x, CellCoords(3, 3))
    assert game.get_result() is GameState.O_WON


def test_check_antidiagonal_losing(game):
    o = PLAYER_MARKS[1]
    game.try_place_marker(o, CellCoords(9, 0))
    game.try_place_marker(o, CellCoords(8, 1))
    game.try_place_marker(o, CellCoords(5, 4))
    game.try_place_marker(o, CellCoords(6, 3))
    game.try_place_marker(o, CellCoords(7, 2))
    assert game.get_result() is GameState.X_WON


def test_check_tie(game):
    x, o = PLAYER_MARKS[0], PLAYER_MARKS[1]

    for row in range(game.width):
        for col in range(game.height):
            if row % 2 == 0:
                game.try_place_marker(x if col % 4 in (0, 1) else o, CellCoords(row, col))
            else:
                game.try_place_marker(o if col % 4 in (0, 1) else x, CellCoords(row, col))
    assert game.get_result() is GameState.TIE
