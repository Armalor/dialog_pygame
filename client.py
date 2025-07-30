from threading import Thread, Lock
import socket
import pygame
import socket
import threading
from net import Net

from spaceship import Spaceship
from bullet import BulletRegistry, Bullet

WIDTH = 1200   # ширина игрового окна
HEIGHT = 1000  # высота игрового окна
FPS = 30  # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def handle_client(sock: socket.socket):
    while True:
        data = sock.recv(1024 * 1024)
        if data:
            print(f'*** {data.decode()}')


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    client = Net.get_local_ip()
    print(f'local IP: {client}')
    host = Net.scan()
    print(f'server host: {host}')
    sock.connect((host, Net.SERVER_PORT))  # подключемся к серверному сокету

    t = Thread(target=handle_client, args=(sock, ), daemon=True)
    t.start()


if __name__ == '__main__':
    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    # Внимание! Мы можем создавать класс Spaceship только ПОСЛЕ инициализации screen!
    ship = Spaceship(velocity=20, screen=screen)

    server_thread = threading.Thread(target=client)
    server_thread.start()

    running = True
    while running:
        clock.tick(FPS)

        # Рендеринг
        screen.fill(BLACK)

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         print(f'right: {pygame.K_RIGHT}')
            # else:
            #     color = GREEN

        keys = pygame.key.get_pressed()
        ship.move(keys)
        ship.draw()

        for bullet in BulletRegistry.bullets:  # type: Bullet
            bullet.move()
            bullet.draw()

        # print(len(BulletRegistry.bullets))

        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()
