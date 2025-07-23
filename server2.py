import pygame, socket, threading
from time import perf_counter
from random import randint
from json import dumps
from spaceship import Spaceship, Bullet, Enemy, update, collusion, enemies, bullets

WIDTH = HEIGHT = 800
FPS = 30

HOST, PORT = '', 35000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f'Server listening on {HOST}:{PORT}')


def handle_client(client_socket: socket.socket):
    while True:
        bullets_to_client = []
        for bullet in bullets:
            b = bullet.to_bytes()
            bullets_to_client.append(b)

        if bullets_to_client:
            client_socket.sendall(dumps(bullets_to_client).encode())


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST = ""
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        thread.start()


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    ship = Spaceship(velocity=10, screen=screen, image='images/spaceship.png')
    running = True
    t0 = perf_counter()

    server_thread = threading.Thread(target=server)
    server_thread.start()

    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        draw_bullet = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    draw_bullet = True

        if draw_bullet:
            b = Bullet(-20, ship.texture_rect.center[0] + 1, ship.texture_rect.center[1] - 70, screen)

        update()

        for b in bullets:
            b.move()
            b.draw()

        keys = pygame.key.get_pressed()
        ship.move(keys)
        ship.draw()
        # print(bullets)

        pygame.display.flip()


if __name__ == '__main__':
    main()
