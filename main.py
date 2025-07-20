import random

import pygame
from time import perf_counter
from spaceship import Spaceship
from spaceship import Bullet, bullets, Enemy, enemies

WIDTH = 1200
HEIGHT = 700
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

t0 = perf_counter()

if __name__ == '__main__':
    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    ship = Spaceship(velocity=20, screen=screen)

    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        drawing_bullet = False  # рисовать ли очередную пулю
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:       # Рисовать пулю, только если отпущен пробел!!!
                if event.key == pygame.K_SPACE:  #                                            |
                    drawing_bullet = True  # <------------------------------------------------

        keys = pygame.key.get_pressed()

        if drawing_bullet:
            # Добавление новой пули в список пуль (немного подгоняются координаты)
            Bullet(-10, ship.texture_rect.center[0] + 1, ship.texture_rect.center[1] - 70, screen)

        if int(t0) % 5 == 0:
            Enemy(5, random.randint(100, WIDTH - 100), 100, screen)

        for bullet in bullets:  # проходимся по всем пулям, двигаем их и рисуем
            bullet.move()
            bullet.draw()

        for enemy in enemies:
            enemy.draw()
            enemy.move()

        ship.move(keys)
        ship.draw()

        pygame.display.flip()
