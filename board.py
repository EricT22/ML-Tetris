import pygame

class Board:

    def __init__(self) -> None:
        self.size = 35
        self.rows = 20
        self.cols = 10
        self.board = [['U' for j in range(self.cols)] for i in range(self.rows)]
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
                tile = pygame.Rect(j * self.size, i * self.size, self.size - 1, self.size - 1)
                pygame.draw.rect(screen, self.colors[self.get_value(i, j)], tile)

    def update_board(self, row, col, value):
        self.board[row][col] = value

    def get_value(self, row, col) -> chr:
        return self.board[row][col]
