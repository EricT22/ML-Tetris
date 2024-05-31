import pygame, sys, cfg
from tetris_game import Tetris_Game

pygame.init()

screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption("Tetris")
pygame.event.set_blocked(pygame.NOEVENT)

clock = pygame.time.Clock()
tetris = Tetris_Game()

TETRIS_UPDATE = pygame.USEREVENT
pygame.time.set_timer(TETRIS_UPDATE, 500)

run = True

while run:
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
            elif event.key == pygame.K_UP:
                tetris.rotate_piece(True)
            elif event.key == pygame.K_z:
                tetris.rotate_piece(False)
            elif event.key == pygame.K_r and tetris.game_over:
                tetris.restart_game()
        elif event.type == TETRIS_UPDATE and not tetris.game_over:
            tetris.move_piece_down()
                
    screen.fill(cfg.MAIN_BACKGROUND_COLOR)
    tetris.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()