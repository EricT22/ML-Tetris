import pygame

class Board:

    def __init__(self) -> None:
        self.size = 35
        self.rows = 20
        self.cols = 10
        self.board = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                tile = pygame.Rect(j * self.size, i * self.size, self.size - 1, self.size - 1)
                pygame.draw.rect(screen, (60, 130, 200), tile)
