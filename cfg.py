from collections import namedtuple

# ML Constants 
Transition = namedtuple('Transition',
                        ('state', 'action', 'reward', 'next_state', 'done'))

CHECKPOINT_FILE_PATH = 'checkpoint.tar'

BATCH_SIZE = 64

MAX_MEMORY_SIZE = 20000

GAMMA = 0.95
EPSILON = 1
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.9908319448927676 # Gets epsilon equal to the min epsilon val after lowering epsilon 500 times
SGD_LEARNING_RATE = 0.01

# Tetris Constants
WIDTH = 950
HEIGHT = 750

TETRIS_TILE_SIZE = 35
TETRIS_ROWS = 20
TETRIS_COLS = 10

MAIN_BOARD_X_OFFSET = (WIDTH - TETRIS_TILE_SIZE * TETRIS_COLS) / 2
MAIN_BOARD_Y_OFFSET = (HEIGHT - TETRIS_TILE_SIZE * TETRIS_ROWS) / 2


SQUARE_PANEL_SIZE = 5

NEXT_PANEL_X_OFFSET = (TETRIS_TILE_SIZE * TETRIS_COLS) + MAIN_BOARD_X_OFFSET + (MAIN_BOARD_X_OFFSET - TETRIS_TILE_SIZE * SQUARE_PANEL_SIZE) / 2
NEXT_PANEL_Y_OFFSET = (HEIGHT - TETRIS_TILE_SIZE * SQUARE_PANEL_SIZE) / 2

HOLD_PANEL_X_OFFSET = (MAIN_BOARD_X_OFFSET - TETRIS_TILE_SIZE * SQUARE_PANEL_SIZE) / 2
HOLD_PANEL_Y_OFFSET = HEIGHT / 7


PIECE_STARTING_X = 4
PIECE_STARTING_Y = 1

DEFAULT_ORIENTATION = 0

PIECE_SIDE_PANEL_X = 2
PIECE_SIDE_PANEL_Y = 2

SCORE_PER_MOVE_DOWN = 1
SCORE_PER_AUTO_DOWN = 2

LINES_PER_LEVEL_UP = 10
TICK_SPEED_MULTIPLIER = 50
STARTING_TICK_SPEED = 1000 # in milliseconds
FASTEST_TICK_SPEED = 17 # in milliseconds (roughly equivalent to 60fps)

# COLORS
MAIN_BACKGROUND_COLOR = "#29303b"
FIELDS_COLOR = "#3e4756"

MEDIUM_BLUE = (60, 130, 200)
PURPLE = (155, 0, 228)
ORANGE = (255, 200, 0)
REGULAR_BLUE = (0, 0, 255)
SKY_BLUE = (30, 220, 252)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COOL_WHITE = "#ddf2ff"