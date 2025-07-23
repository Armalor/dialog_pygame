import json
import pygame
import socket
import threading
from net import Net
from  time import sleep

from spaceship import Spaceship
from bullet import  Bullet, bullets

WIDTH = 800   # ширина игрового окна
HEIGHT = 800  # высота игрового окна
FPS = 30      # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def handle_client(client_socket: socket.socket, c):
    while True:
        bullets_to_client = []
        for bullet in bullets:
            b = {'type': 'b'}
            b['x'] = bullet.texture_rect.center[0]
            b['y'] = bullet.texture_rect.center[1]
            bullets_to_client.append(b)

        if bullets_to_client:
            client_socket.sendall(json.dumps(bullets_to_client).encode())
            sleep(1/30.0)


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
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SERVER")
    clock = pygame.time.Clock()
    ship = Spaceship(velocity=20, screen=screen)
    running = True

    server_thread = threading.Thread(target=server)
    server_thread.start()

    while running:
        clock.tick(FPS)

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        keys = pygame.key.get_pressed()
        ship.move(keys)
        ship.draw()

        for bullet in bullets:  # type: Bullet
            bullet.move()
            bullet.draw()

        pygame.display.flip()
