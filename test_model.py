from game import Bot, InverseTicTacToeBoard, PlayerMark, CellCoords, GameState
import pytest


@pytest.fixture(autouse=True)
def board():
    board = InverseTicTacToeBoard(col_count=10, row_count=10, losing_length=5)
    yield board


def test_params_boundary_values():
    with pytest.raises(ValueError):
        InverseTicTacToeBoard(col_count=0, row_count=10, losing_length=5)
    with pytest.raises(ValueError):
        InverseTicTacToeBoard(col_count=0, row_count=0, losing_length=5)
    with pytest.raises(ValueError):
        InverseTicTacToeBoard(col_count=10, row_count=10, losing_length=11)


def test_placing_markers(board):
    x = PlayerMark.X
    o = PlayerMark.O
    board.try_place_marker(x, CellCoords(1, 1))
    board.try_place_marker(o, CellCoords(2, 2))
    assert board._InverseTicTacToeBoard__board[1][1] is PlayerMark.X
    assert board._InverseTicTacToeBoard__board[2][2] is PlayerMark.O
    assert board.get_result() is GameState.IN_PROGRESS
    # check if player can't place a marker when cell is not empty
    assert board.try_place_marker(x, CellCoords(1, 1)) is False
    assert board.try_place_marker(o, CellCoords(2, 2)) is False
    # bounds check
    assert board.try_place_marker(x, CellCoords(-1, -1)) is False
    assert board.try_place_marker(x, CellCoords(0, 0)) is True
    assert board.try_place_marker(x, CellCoords(-1, 10)) is False
    assert board.try_place_marker(x, CellCoords(0, 9)) is True
    assert board.try_place_marker(x, CellCoords(10, -1)) is False
    assert board.try_place_marker(x, CellCoords(9, 0)) is True
    assert board.try_place_marker(x, CellCoords(10, 10)) is False
    assert board.try_place_marker(x, CellCoords(9, 9)) is True


def test_check_horizontal_losing(board):
    x = PlayerMark.X
    board.try_place_marker(x, CellCoords(1, 1))
    board.try_place_marker(x, CellCoords(1, 2))
    board.try_place_marker(x, CellCoords(1, 5))
    board.try_place_marker(x, CellCoords(1, 4))
    board.try_place_marker(x, CellCoords(1, 3))
    assert board.get_result() is GameState.O_WON


def test_check_vertical_losing(board):
    o = PlayerMark.O
    board.try_place_marker(o, CellCoords(2, 4))
    board.try_place_marker(o, CellCoords(3, 4))
    board.try_place_marker(o, CellCoords(6, 4))
    board.try_place_marker(o, CellCoords(5, 4))
    board.try_place_marker(o, CellCoords(4, 4))
    assert board.get_result() is GameState.X_WON


def test_check_main_diagonal_losing(board):
    x = PlayerMark.X
    board.try_place_marker(x, CellCoords(1, 1))
    board.try_place_marker(x, CellCoords(2, 2))
    board.try_place_marker(x, CellCoords(5, 5))
    board.try_place_marker(x, CellCoords(4, 4))
    board.try_place_marker(x, CellCoords(3, 3))
    assert board.get_result() is GameState.O_WON


def test_check_antidiagonal_losing(board):
    o = PlayerMark.O
    board.try_place_marker(o, CellCoords(9, 0))
    board.try_place_marker(o, CellCoords(8, 1))
    board.try_place_marker(o, CellCoords(5, 4))
    board.try_place_marker(o, CellCoords(6, 3))
    board.try_place_marker(o, CellCoords(7, 2))
    assert board.get_result() is GameState.X_WON


def test_check_tie(board):
    x, o = PlayerMark.X, PlayerMark.O
    for row in range(board.col_count):
        for col in range(board.row_count):
            if row % 2 == 0:
                board.try_place_marker(
                    x if col % 4 in (0, 1) else o, CellCoords(row, col)
                )
            else:
                board.try_place_marker(
                    o if col % 4 in (0, 1) else x, CellCoords(row, col)
                )
    assert board.get_result() is GameState.TIE


def test_bot_doesnt_lose(board):
    bot1 = Bot(board, marker=PlayerMark.X)
    bot2 = Bot(board, marker=PlayerMark.O)
    for _ in range(50):
        bot1.make_a_move()
        bot2.make_a_move()
    assert board.get_result() is GameState.TIE
