import sys
import pygame
from game import PlayerMark, InverseTicTacToeBoard, Bot, CellCoords, GameState
# initialize pygame
pygame.init()


CELL_SIZE = 50
MARGIN = 1
ROW_COUNT, COL_COUNT = 10, 10
LOSING_LENGTH = 5
SCREEN_WIDTH = CELL_SIZE * COL_COUNT + MARGIN * (COL_COUNT + 1)
SCREEN_HEIGHT = CELL_SIZE * ROW_COUNT + MARGIN * (ROW_COUNT + 1)
FONT_NAME = 'arial'

# colors
CELL_COLOR = (240, 240, 240)
O_COLOR = (0, 150, 0)
X_COLOR = (0, 0, 255)
BG_COLOR = (100, 100, 100)
GAME_OVER_BG_COLOR = (0, 0, 0)


screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inverse Tic-Tac-Toe")
img = pygame.image.load("tic-tac-toe.png")
pygame.display.set_icon(img)

game_over = False
board = InverseTicTacToeBoard(
    width=COL_COUNT, height=ROW_COUNT, losing_length=LOSING_LENGTH)
bot = Bot(board, marker=PlayerMark.O)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            col = x_mouse // (MARGIN + CELL_SIZE)
            row = y_mouse // (MARGIN + CELL_SIZE)
            cell = CellCoords(row, col)
            if board.try_place_marker(PlayerMark.X, cell):
                bot.make_a_move()
        elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            board = InverseTicTacToeBoard(
                width=COL_COUNT, height=ROW_COUNT, losing_length=LOSING_LENGTH)
            bot = Bot(board, marker=PlayerMark.O)

    if not game_over:
        screen.fill(BG_COLOR)
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                x = col * CELL_SIZE + (col + 1) * MARGIN
                y = row * CELL_SIZE + (row + 1) * MARGIN
                pygame.draw.rect(screen, CELL_COLOR,
                                 (x, y, CELL_SIZE, CELL_SIZE))
                # FIXME board.current_player ??
                if board._InverseTicTacToeBoard__board[row][col] == PlayerMark.X:
                    pygame.draw.line(
                        screen,
                        X_COLOR,
                        (x + 5, y + 5),
                        (x + CELL_SIZE - 5, y + CELL_SIZE - 5),
                        width=5,
                    )
                    pygame.draw.line(
                        screen,
                        X_COLOR,
                        (x + CELL_SIZE - 5, y + 5),
                        (x + 5, y + CELL_SIZE - 5),
                        width=5,
                    )
                elif board._InverseTicTacToeBoard__board[row][col] == PlayerMark.O:
                    pygame.draw.circle(
                        screen,
                        O_COLOR,
                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        radius=CELL_SIZE // 2 - 3,
                        width=3,
                    )

    if board.get_result() is not GameState.IN_PROGRESS:
        game_over = True

    if game_over:
        font = pygame.font.SysFont(FONT_NAME, 50)
        if board.get_result() is GameState.X_WON:
            msg = 'X'
        elif board.get_result() is GameState.O_WON:
            msg = 'O'
        else:
            msg = 'TIE'
        text = font.render(f'{msg} has won!', True, (226, 20, 27))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, (text_x, text_y))
        pygame.display.update()

    pygame.display.update()
