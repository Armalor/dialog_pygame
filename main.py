import json
import os
import pygame
from pygame.key import ScancodeWrapper
import socket
import threading
from queue import Queue
from net import Net

from spaceship import Spaceship, Spaceship2
from bullet import BulletRegistry, Bullet

WIDTH = 1200   # ширина игрового окна
HEIGHT = 1000  # высота игрового окна
FPS = 30  # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


client_server_queue = Queue(maxsize=128)
server_client_queue = Queue(maxsize=128)

clients = dict()

ships = list()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((Net.HOST, Net.SERVER_PORT))
    # server_socket.settimeout(1.0)
    server_socket.listen(2)
    print(f"Server listening on {Net.HOST}:{Net.SERVER_PORT}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()

            clients[client_address[0]] = client_socket

            # thread_sender = threading.Thread(target=server_sender, args=(client_socket, client_address), daemon=True)
            # thread_sender.start()

            thread_receiver = threading.Thread(target=server_receiver, args=(client_socket, client_address), daemon=True)
            thread_receiver.start()

        except socket.timeout:
            print("Socket accept timed out.")
        except Exception as e:
            print(f"An error occurred: {e}")


def server_sender(client_socket: socket.socket, client_address):
    while True:
        ...
        # bullets_to_client = {
        #     'type': 'b',
        #     'data': [],
        # }
        # for bullet in BulletRegistry.bullets:
        #     b = dict()
        #     b['x'] = bullet.texture_rect.center[0]
        #     b['y'] = bullet.texture_rect.center[1]
        #     bullets_to_client['data'].append(b)
        #
        # if bullets_to_client:
        #     client_socket.sendall(json.dumps(bullets_to_client).encode())
    # jsonable = ...


def server_receiver(client_socket: socket.socket, client_address):
    try:
        while True:
            message: str = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            message = json.loads(message)
            if not server_client_queue.full():
                server_client_queue.put(message)

    except Exception as e:
        print(f"Error handling client {client_address} ({type(e)}): {e}")
    finally:
        client_socket.close()
        print(f"Connection from {client_address} closed")


def client() -> socket.socket:
    client_ip = Net.get_local_ip()
    print(f'Client local IP: {client_ip}')
    server_ip = Net.scan()
    print(f'Client looks to server host: {server_ip}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет

    sock.connect((server_ip, Net.SERVER_PORT))

    return sock


def client_receiver(sock: socket.socket):
    while True:
        data = sock.recv(1024*1024)  # читаем ответ от серверного сокета
        if data:
            print(f'*** {data.decode()} ***')
            print('Enter message:')


def client_sender(sock: socket.socket):
    while True:
        message = client_server_queue.get()
        message = json.dumps(message)
        print(f'{message=}')
        sock.send(bytes(message, encoding='UTF-8'))  # отправляем сообщение

        client_server_queue.task_done()


if __name__ == '__main__':

    server_mode = bool(os.getenv('server', '0'))
    print(f'{server_mode=}')

    # создаем игру и окно
    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    # Внимание! Мы можем создавать класс Spaceship только ПОСЛЕ инициализации screen!
    main_ship = Spaceship(velocity=20, screen=screen)
    # ships.append(Spaceship(velocity=20, screen=screen))
    # ships.append(Spaceship2(velocity=20, screen=screen))

    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()

    # Клиентский сокет создаем не в параллельном режиме, т.к. он точно нужен всегда
    client_socket = client()
    client_sender_thread = threading.Thread(target=client_sender, args=(client_socket,), daemon=True)
    client_sender_thread.start()

    running = True
    # Нажатые клавиши не возбуждают события pygme, поэтому при возникновении pygame.KEYDOWN просто помещаем код клавиши
    # во множество текущих нажатых, а при pygame.KEYUP — убираем.
    e_keys = set()

    while running:
        clock.tick(FPS)

        # Рендеринг
        screen.fill(BLACK)

        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False

            # См. выше: нажатые клавиши не возбуждают события pygame, поэтому при возникновении pygame.KEYDOWN
            # просто помещаем код клавиши во множество текущих нажатых,..
            if event.type in [pygame.KEYDOWN]:
                e_keys.add(event.key)

            # а при pygame.KEYUP — убираем.
            if event.type in [pygame.KEYUP]:
                e_keys.discard(event.key)

        # if e_keys and not client_server_queue.full():
        #     client_server_queue.put(list(e_keys))
        #
        # if not server_client_queue.empty():
        #     full_e_keys = server_client_queue.get()
        # else:
        #     full_e_keys = set()

        # keys = pygame.key.get_pressed() нам не подходит, т.к. от возвращает tuple-подобный объект на 512 элементов
        # со сложной схемой __getitem__, позволяющей «проверить» через keys[idx] числа сильно выше 512, например
        # pygame.K_RIGHT == 1073741903

        # main_ship.move(e_keys)

        for ship in ships:
            ship.draw()

        # for bullet in BulletRegistry.bullets:  # type: Bullet
        #     bullet.move()
        #     bullet.draw()

        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()
