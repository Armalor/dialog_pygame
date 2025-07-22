import json
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


def handle_client(client_socket: socket.socket, client_address):
    while True:
        bullets_to_client = []
        for bullet in BulletRegistry.bullets:
            b = {'type': 'b'}
            b['x'] = bullet.texture_rect.center[0]
            b['y'] = bullet.texture_rect.center[1]
            bullets_to_client.append(b)

        if bullets_to_client:
            client_socket.sendall(json.dumps(bullets_to_client).encode())
    # jsonable = ...


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST = ""
    server_socket.bind((HOST, Net.SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{Net.SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        thread.start()


if __name__ == '__main__':
    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    # Внимание! Мы можем создавать класс Spaceship только ПОСЛЕ инициализации screen!
    ship = Spaceship(velocity=20, screen=screen)

    server_thread = threading.Thread(target=server)
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
            #         color = RED
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
