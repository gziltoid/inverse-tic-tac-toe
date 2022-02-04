from game import InverseTicTacToeBoard, PLAYER_MARKS, Coords
from pprint import pprint


def test_try_place_marker():
    game = InverseTicTacToeBoard(5, 5)
    x = PLAYER_MARKS[0]
    o = PLAYER_MARKS[1]
    game.try_place_marker(x, Coords(1, 1))
    game.try_place_marker(x, Coords(2, 2))
    game.try_place_marker(x, Coords(3, 3))
    pprint(game.board)
    print(game.get_result())
    assert game.board[1][1] == 'X', 'Oops!'
    assert game.board[3][3] == 'X', 'Oops!'

