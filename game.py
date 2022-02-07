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
FONT_SIZE = 50

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
    GameState.TIE: "It's a tie!",
}


class InverseTicTacToeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Inverse Tic-Tac-Toe")
        icon_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "tic-tac-toe.png"
        )
        pygame.display.set_icon(pygame.image.load(icon_path))

    def start_new_game(self):
        self.game_over = False
        self.board = InverseTicTacToeBoard(
            width=COL_COUNT, height=ROW_COUNT, losing_length=LOSING_LENGTH
        )
        self.bot = Bot(self.board, marker=PlayerMark.O)

    def run(self):
        self.start_new_game()
        self.draw_grid()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.draw_on_click()
                elif (
                    self.game_over
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                ):
                    self.start_new_game()
                    self.draw_grid()

            # FIXME
            if self.board.get_result() is not GameState.IN_PROGRESS:
                self.game_over = True

            if self.game_over:
                self.show_end_of_game(
                    message=GAME_STATE_MESSAGES[self.board.get_result()]
                )

            pygame.display.flip()

    def __get_cell(self):
        x_m, y_m = pygame.mouse.get_pos()
        col = x_m // (CELL_MARGIN + CELL_SIZE)
        row = y_m // (CELL_MARGIN + CELL_SIZE)
        return CellCoords(row, col)

    def draw_on_click(self):
        cell = self.__get_cell()
        if self.board.try_place_marker(PlayerMark.X, cell):
            self.draw_marker(PlayerMark.X, cell)
            if bot_move := self.bot.make_a_move():
                self.draw_marker(PlayerMark.O, bot_move)

    def draw_grid(self):
        self.screen.fill(BG_COLOR)
        # for row in range(ROW_COUNT):
        #     for col in range(COL_COUNT):
        #         x = col * CELL_SIZE + (col + 1) * CELL_MARGIN
        #         y = row * CELL_SIZE + (row + 1) * CELL_MARGIN
        #         pygame.draw.rect(self.screen, CELL_COLOR,
        #                          (x, y, CELL_SIZE, CELL_SIZE))
        for i in range(1, COL_COUNT):
            x = i * CELL_SIZE + (i + 1) * CELL_MARGIN
            pygame.draw.line(
                self.screen, GRID_COLOR, (0, x), (SCREEN_WIDTH, x), width=CELL_MARGIN
            )
        for i in range(1, ROW_COUNT):
            y = i * CELL_SIZE + (i + 1) * CELL_MARGIN
            pygame.draw.line(
                self.screen, GRID_COLOR, (y, 0), (y, SCREEN_HEIGHT), width=CELL_MARGIN
            )

    def draw_marker(self, marker, pos):
        x = pos.col * CELL_SIZE + (pos.col + 1) * CELL_MARGIN
        y = pos.row * CELL_SIZE + (pos.row + 1) * CELL_MARGIN
        if marker == PlayerMark.X:
            pygame.draw.line(
                self.screen,
                X_COLOR,
                (x + 5, y + 5),
                (x + CELL_SIZE - 5, y + CELL_SIZE - 5),
                width=5,
            )
            pygame.draw.line(
                self.screen,
                X_COLOR,
                (x + CELL_SIZE - 5, y + 5),
                (x + 5, y + CELL_SIZE - 5),
                width=5,
            )
        else:
            pygame.draw.circle(
                self.screen,
                O_COLOR,
                (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                radius=CELL_SIZE // 2 - 3,
                width=3,
            )

    def show_end_of_game(self, message):
        # TODO loser's crossing line
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        text = font.render(message, True, FONT_COLOR)
        text_x = (self.screen.get_width() - text.get_width()) // 2
        text_y = (self.screen.get_height() - text.get_height()) // 2
        self.screen.blit(text, (text_x, text_y))


if __name__ == "__main__":
    game = InverseTicTacToeGame()
    game.run()
