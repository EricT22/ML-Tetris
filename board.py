import pygame, cfg

class Board_Panel:

    def __init__(self, tile_size: int, rows: int, cols: int, x_offset: int, y_offset: int) -> None:
        self.tile_size = tile_size
        self.rows = rows
        self.cols = cols
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.game_board = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.colors = {
            0 : cfg.MEDIUM_BLUE, # empty
            1 : cfg.PURPLE, # T
            2 : cfg.ORANGE, # L
            3 : cfg.REGULAR_BLUE, # J
            4 : cfg.SKY_BLUE, # I
            5 : cfg.YELLOW, # O
            6 : cfg.GREEN, # S
            7 : cfg.RED # Z
        }


    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                tile = pygame.Rect(j * self.tile_size + self.x_offset, i * self.tile_size + self.y_offset, 
                                   self.tile_size - 1, self.tile_size - 1)
                pygame.draw.rect(screen, self.colors[self.get_value(i, j)], tile)


    def update_board(self, row, col, value):
        self.game_board[row][col] = value


    def get_value(self, row, col) -> int:
        if row < 0 or col < 0:
            raise IndexError

        return self.game_board[row][col]
    

    def clear(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.update_board(row, col, 0)

    def copy_of_board(self):
        return [row[:] for row in self.game_board]



    # debugging only (for now, ill use it for machine learning later)
    def print(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.game_board[i][j], end=" ")
            print("")