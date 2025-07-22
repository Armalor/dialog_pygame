from threading import Thread, Lock
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет

from net import Net

client = Net.get_local_ip()
print(f'local IP: {client}')
host = Net.scan()


def receive(sock: socket.socket):
    while True:
        data = sock.recv(1024)  # читаем ответ от серверного сокета
        if data:
            print(f'\r*** {data.decode()}')
            print('Enter message:')


if host:
    print(f'server host: {host}')
    sock.connect((host, Net.SERVER_PORT))  # подключемся к серверному сокету

    t = Thread(target=receive, args=(sock, ), daemon=True)
    t.start()

    while True:
        message = input('Enter message:')
        sock.send(bytes(message, encoding='UTF-8'))  # отправляем сообщение

    # sock.close()  # закрываем соединение
