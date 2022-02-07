#!/usr/bin/env python3
import sys
import os
import pygame
from model import PlayerMark, InverseTicTacToeBoard, Bot, CellCoords, GameState


ROW_COUNT, COL_COUNT = 10, 10
LOSING_LENGTH = 5

CELL_SIZE = 50
CELL_MARGIN = 1
SCREEN_WIDTH = CELL_SIZE * COL_COUNT + CELL_MARGIN * (COL_COUNT + 1)
SCREEN_HEIGHT = CELL_SIZE * ROW_COUNT + CELL_MARGIN * (ROW_COUNT + 1)
FONT_NAME = "arial"
FONT_SIZE = SCREEN_WIDTH // 8

# colors
GRID_COLOR = (0, 0, 0)
O_COLOR = (0, 150, 0)
X_COLOR = (0, 0, 255)
BG_COLOR = (230, 230, 230)
GAME_OVER_BG_COLOR = (0, 0, 0)
FONT_COLOR = (226, 20, 27)

GAME_STATE_MESSAGES = {
    GameState.X_WON: "X has won!",
    GameState.O_WON: "O has won!",
    GameState.TIE: "TIE!",
}


class InverseTicTacToeGame:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Inverse Tic-Tac-Toe")
        icon_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "tic-tac-toe.png"
        )
        pygame.display.set_icon(pygame.image.load(icon_path))

    def __start_new_game(self):
        self.__game_over = False
        self.__board = InverseTicTacToeBoard(
            col_count=COL_COUNT, row_count=ROW_COUNT, losing_length=LOSING_LENGTH
        )
        self.__bot = Bot(self.__board, marker=PlayerMark.O)

    def run(self):
        self.__start_new_game()
        self.__draw_grid()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.__game_over:
                    self.__on_click()
                elif (
                    self.__game_over
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                ):
                    self.__start_new_game()
                    self.__draw_grid()

            if self.__game_over:
                self.__show_end_of_game(
                    message=GAME_STATE_MESSAGES[self.__board.get_result()]
                )

            pygame.display.flip()

    def __get_cell_under_cursor(self):
        x_m, y_m = pygame.mouse.get_pos()
        col = x_m // (CELL_MARGIN + CELL_SIZE)
        row = y_m // (CELL_MARGIN + CELL_SIZE)
        return CellCoords(row, col)

    def __on_click(self):
        cell = self.__get_cell_under_cursor()
        if self.__board.try_place_marker(PlayerMark.X, cell):
            self.__draw_marker(PlayerMark.X, cell)
            if bot_move := self.__bot.make_a_move():
                self.__draw_marker(PlayerMark.O, bot_move)
        if self.__board.get_result() is not GameState.IN_PROGRESS:
            self.__game_over = True

    def __draw_grid(self):
        self.__screen.fill(BG_COLOR)
        # draw horizontal lines
        for i in range(1, ROW_COUNT):
            y = i * CELL_SIZE + (i + 1) * CELL_MARGIN
            pygame.draw.line(
                self.__screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), width=CELL_MARGIN
            )
        # draw vertical lines
        for i in range(1, COL_COUNT):
            x = i * CELL_SIZE + (i + 1) * CELL_MARGIN
            pygame.draw.line(
                self.__screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), width=CELL_MARGIN
            )

    def __draw_marker(self, marker, pos):
        x = pos.col * CELL_SIZE + (pos.col + 1) * CELL_MARGIN
        y = pos.row * CELL_SIZE + (pos.row + 1) * CELL_MARGIN
        if marker == PlayerMark.X:
            pygame.draw.line(
                self.__screen,
                X_COLOR,
                (x + 5, y + 5),
                (x + CELL_SIZE - 5, y + CELL_SIZE - 5),
                width=5,
            )
            pygame.draw.line(
                self.__screen,
                X_COLOR,
                (x + CELL_SIZE - 5, y + 5),
                (x + 5, y + CELL_SIZE - 5),
                width=5,
            )
        else:
            pygame.draw.circle(
                self.__screen,
                O_COLOR,
                (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                radius=CELL_SIZE // 2 - 3,
                width=3,
            )

    def __show_end_of_game(self, message):
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        text = font.render(message, True, FONT_COLOR)
        text_x = (self.__screen.get_width() - text.get_width()) // 2
        text_y = (self.__screen.get_height() - text.get_height()) // 2
        self.__screen.blit(text, (text_x, text_y))


if __name__ == "__main__":
    try:
        game = InverseTicTacToeGame()
        game.run()
    except Exception as e:
        sys.stderr.write(f"Exception: {e}" + os.linesep)
