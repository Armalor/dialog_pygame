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
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет

from net import Net
data_lis = {}
client = Net.get_local_ip()
print(f'local IP: {client}')
host = Net.scan()


def receive(sock: socket.socket):
    global data_lis
    while True:
        data = sock.recv(1024000)  # читаем ответ от серверного сокета
        data_lis = json.loads(data.decode())
        # if data:
            # print(f'*** {data.decode()}')




    # while True:
    #     message = input('Enter message:')
    #     sock.send(bytes(message, encoding='UTF-8'))  # отправляем сообщение







WIDTH = 1200   # ширина игрового окна
HEIGHT = 700  # высота игрового окна
FPS = 30  # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



if __name__ == '__main__':

    if host:
        print(f'server host: {host}')
        sock.connect((host, Net.SERVER_PORT))  # подключемся к серверному сокету

        t = threading.Thread(target=receive, args=(sock,), daemon=True)
        t.start()

    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Внимание! Мы можем создавать класс Spaceship только ПОСЛЕ инициализации screen!

    ship1 = Spaceship(velocity=20, screen=screen)
    ship2 = Spaceship2(velocity=20, screen=screen)
    pygame.display.set_caption("My Game 111")
    clock = pygame.time.Clock()

    running = True
    while running:
        print(f'{data_lis=}')
        if 'x' in data_lis and 'y' in data_lis:
            enemy = Enemy1(data_lis.get("x"), data_lis.get("y"), velocity=10, screen=screen)

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



        for enemy in Enemyregister.enemies:
            enemy.draw()
            for bullet in BulletRegistry.bullets:
                enemy.test_die(bullet.texture_rect)

        for bullet in BulletRegistry.bullets:  # type: Bullet
            bullet.move()
            bullet.draw()





        # print(len(BulletRegistry.bullets))

        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()
