import pygame, sys, cfg
import matplotlib.pyplot as plt
import numpy as np
from tetris_game import Tetris_Game
from agent import Agent

pygame.init()

screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption("Tetris")
pygame.event.set_blocked(pygame.NOEVENT)


label_font = pygame.font.Font(None, 50)
next_label_surface = label_font.render("NEXT", True, cfg.COOL_WHITE)
hold_label_surface = label_font.render("HOLD", True, cfg.COOL_WHITE)
level_label_surface = label_font.render("LEVEL", True, cfg.COOL_WHITE)
score_label_surface = label_font.render("SCORE", True, cfg.COOL_WHITE)
lines_label_surface = label_font.render("LINES", True, cfg.COOL_WHITE)

field_value_font = pygame.font.Font(None, 25)
level_field = pygame.Rect(63, 425, 175, 40)
score_field = pygame.Rect(63, 550, 175, 40)
lines_field = pygame.Rect(63, 675, 175, 40)


clock = pygame.time.Clock()
tetris = Tetris_Game()

TETRIS_UPDATE = pygame.USEREVENT
pygame.time.set_timer(TETRIS_UPDATE, cfg.STARTING_TICK_SPEED)


def render(extra_info=True):
    # Extra info can be ommitted if its too slow
    if extra_info:
        screen.fill(cfg.MAIN_BACKGROUND_COLOR)

        screen.blit(next_label_surface, (756, 150))

        screen.blit(hold_label_surface, (100, 40))


        screen.blit(level_label_surface, (97, 375))
        pygame.draw.rect(screen, cfg.FIELDS_COLOR, level_field, 0, 5)
        level_field_value = field_value_font.render(str(tetris.level), True, cfg.COOL_WHITE)
        screen.blit(level_field_value, level_field_value.get_rect(centerx = level_field.centerx, centery = level_field.centery))


        screen.blit(score_label_surface, (92, 500))
        pygame.draw.rect(screen, cfg.FIELDS_COLOR, score_field, 0, 5)
        score_field_value = field_value_font.render(str(tetris.score), True, cfg.COOL_WHITE)
        screen.blit(score_field_value, score_field_value.get_rect(centerx = score_field.centerx, centery = score_field.centery))

        screen.blit(lines_label_surface, (102, 625))
        pygame.draw.rect(screen, cfg.FIELDS_COLOR, lines_field, 0, 5)
        lines_field_value = field_value_font.render(str(tetris.lines), True, cfg.COOL_WHITE)
        screen.blit(lines_field_value, lines_field_value.get_rect(centerx = lines_field.centerx, centery = lines_field.centery))
    
    tetris.draw(screen)

    pygame.display.update()


def update_tick_speed():
    if tetris.level_up_triggered:
            new_tick_speed = cfg.STARTING_TICK_SPEED - (cfg.TICK_SPEED_MULTIPLIER * (tetris.level - 1))

            pygame.time.set_timer(TETRIS_UPDATE, cfg.FASTEST_TICK_SPEED if new_tick_speed < cfg.FASTEST_TICK_SPEED else new_tick_speed)

            tetris.level_up_triggered = False


def on_close(event):
    sys.exit()


def plot_final_scores(scores):
    games = np.arange(len(scores)) + 1

    plt.figure(figsize=(12, 6)).canvas.mpl_connect('close_event', on_close)
    plt.plot(games, scores, marker='o')
    plt.xlabel("Games", size=22.5)
    plt.ylabel("Final Score", size=22.5)
    plt.show()




# NOTE: Agent doesn't learn in game loop, just plays according to what it has

if __name__ == "__main__":
    final_scores = []

    agent = Agent(env=tetris, greedy_epsilon=0)
    state = tetris.reset()
    
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == TETRIS_UPDATE and not tetris.game_over:
                tetris.move_piece_down(0)

                action, next_state = agent.choose_action(tetris.get_next_states())

                reward, done = tetris.step(action)

                if done:
                    final_scores.append(tetris.score)

                    state = tetris.reset()
                    
        

        render()

        update_tick_speed()

        
        clock.tick(60)

    pygame.quit()

    plot_final_scores(final_scores)