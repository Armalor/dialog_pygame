import random
import pygame
from time import perf_counter, sleep
from spaceship import Spaceship
from spaceship import Bullet, bullets, Enemy, enemies, update, collusion

WIDTH = 800
HEIGHT = 800
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

if __name__ == '__main__':
    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    ship = Spaceship(velocity=10, screen=screen)

    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    t0 = perf_counter()

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        drawing_bullet = False  # рисовать ли очередную пулю
        drawing_enemy = False

        if not ship.alive:
            screen.fill(RED)  # Заполняем экран красным цветом
            print('Проигрыш')
            sleep(2)

            break

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

        if perf_counter() - t0 > 1:
            t0 = perf_counter()
            Enemy(3, random.randint(100, WIDTH - 100), 100, screen)

        collusion(ship, HEIGHT)  # проверить столкноевение корабля и врагов и врагов и пуль
        update()  # обновить список

        for bullet in bullets:  # проходимся по всем пулям, двигаем их и рисуем
            bullet.move()
            bullet.draw()

        for enemy in enemies:
            enemy.draw()
            enemy.move()

        ship.move(keys)
        ship.draw()

        pygame.display.flip()
