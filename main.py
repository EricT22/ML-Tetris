import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

square = pygame.Rect((300, 250, 50, 50))

run = True

while run:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), square)

    key = pygame.key.get_pressed()

    if key[pygame.K_a] == True:
        square.move_ip(-1, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()