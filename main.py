import pygame
import random as r
from enemy import Enemy1, Enemyregister
from spaceship import Spaceship
from spaceship2 import Spaceship2
from bullet import BulletRegistry, Bullet
import  json
# from example0_server import *
import socket
from net import Net
import threading
import os

is_server = int(os.getenv('server', 0))
print(f'{is_server=}')

WIDTH = 1200   # ширина игрового окна
HEIGHT = 700  # высота игрового окна
FPS = 30# частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def handle_client(client_socket: socket.socket, client_address):
    while True:
        enemy_to_client = []
        for enemy in Enemyregister.enemies:
            e = {'type': 'e'}
            e['x'] = enemy.texture_rect.center[0]
            e['y'] = enemy.texture_rect.center[1]
            enemy_to_client.append(e)
            # print(enemy_to_client)
        if enemy_to_client:
            client_socket.sendall(json.dumps(enemy_to_client).encode())
            print(enemy_to_client)


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

    # Внимание! Мы можем создавать класс Spaceship только ПОСЛЕ инициализации screen!

    ship1 = Spaceship(velocity=20, screen=screen)
    ship2 = Spaceship2(velocity=20, screen=screen)
    enemy = Enemy1(r.randint(1, 1200), -10, velocity=10, screen=screen)
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    s_thread = threading.Thread(target=server, daemon=True)
    s_thread.start()

    running = True
    while running:
        clock.tick(FPS)

        screen.fill(BLACK)

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        ship1.move(keys)
        ship1.draw()
        ship2.move(keys)
        ship2.draw()
        enemy.spawn()


        for enemy in Enemyregister.enemies:
            for bullet in BulletRegistry.bullets:
                enemy.test_die(bullet.texture_rect)

        for bullet in BulletRegistry.bullets:  # type: Bullet
            bullet.move()
            bullet.draw()

        for enemy in Enemyregister.enemies:
            enemy.move()
            enemy.draw()



        # print(len(BulletRegistry.bullets))

        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()
