import pygame
from tetris_game import Tetris_Game

pygame.init()

WIDTH = 350
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

tetris = Tetris_Game()

run = True

while run:
    screen.fill((0, 0, 0))
    tetris.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()