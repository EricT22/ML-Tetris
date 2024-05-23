import pygame
from tetris_game import Tetris_Game

pygame.init()

WIDTH = 350
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
pygame.event.set_blocked(pygame.NOEVENT)

clock = pygame.time.Clock()
tetris = Tetris_Game()

run = True

# TODO: something here about drawing first updating the moves later and updating the screen after one tick that's unsettling
while run:
    screen.fill((0, 0, 0))
    tetris.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tetris.move_piece_down()
            elif event.key == pygame.K_SPACE:
                tetris.auto_down()
            elif event.key == pygame.K_RIGHT:
                tetris.move_piece_sideways(True)
            elif event.key == pygame.K_LEFT:
                tetris.move_piece_sideways(False)

    pygame.display.update()
    pygame.event.clear()
    clock.tick(60)

pygame.quit()