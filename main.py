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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tetris.move_piece_down()
            elif event.key == pygame.K_SPACE:
                tetris.auto_down()
            elif event.key == pygame.K_RIGHT:
                tetris.move_piece_sideways(True)
            elif event.key == pygame.K_LEFT:
                tetris.move_piece_sideways(False)
            elif event.key == pygame.K_UP:
                tetris.rotate_piece(True)
            elif event.key == pygame.K_z:
                tetris.rotate_piece(False)
                
    screen.fill((0, 0, 0))
    tetris.draw(screen)

    pygame.display.update()
    pygame.event.clear()
    clock.tick(60)