import pygame
import random

from spaceship import Spaceship

WIDTH = 1200   # ширина игрового окна
HEIGHT = 1000  # высота игрового окна
FPS = 30  # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SPACESKY = (0, 0, 15)

if __name__ == '__main__':
    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Внимание! Мы можем создавать класс Spaceship только ПОСЛЕ инициализации screen!

    ship = Spaceship(velocity=20, screen=screen)

    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        # Рендеринг
        screen.fill(SPACESKY)

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         color = RED
            # else:
            #     color = GREEN

        keys = pygame.key.get_pressed()
        ship.move(keys)
        ship.draw()

        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()
