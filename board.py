import pygame

class Board_Panel:

    def __init__(self, tile_size: int, rows: int, cols: int, x_offset: int, y_offset: int) -> None:
        self.tile_size = tile_size
        self.rows = rows
        self.cols = cols
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.game_board = [['U' for j in range(self.cols)] for i in range(self.rows)]
        self.colors = {
            'U': (60, 130, 200), # unassigned - medium blue
            'T': (155, 0, 228), # purple
            'L': (255, 200, 0), # orange
            'J': (0, 0, 255), # blue
            'I': (30, 220, 252), # sky blue
            'O': (255, 255, 0), # yellow
            'S': (0, 255, 0), # green
            'Z': (255, 0, 0) # red
        }


    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                tile = pygame.Rect(j * self.tile_size + self.x_offset, i * self.tile_size + self.y_offset, 
                                   self.tile_size - 1, self.tile_size - 1)
                pygame.draw.rect(screen, self.colors[self.get_value(i, j)], tile)


    def update_board(self, row, col, value):
        self.game_board[row][col] = value


    def get_value(self, row, col) -> chr:
        if row < 0 or col < 0:
            raise IndexError

        return self.game_board[row][col]
    

    def clear(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.update_board(row, col, 'U')


    # debugging only (for now, ill use it for machine learning later)
    def print(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.game_board[i][j], end=" ")
            print("")