import socket
from threading import Thread, Lock
from time import sleep
import random
from net import Net


blocker = Lock()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет


def in_thread(stop=1000_000, name=None):
    while True:
        data = sock.recv(102400)  # читаем ответ от серверного сокета
        print(data.decode())




if __name__ == '__main__':


    client = Net.get_local_ip()
    print(f'local IP: {client}')
    host = Net.scan()
    if host:
        print(f'server host: {host}')
        sock.connect((host, 33_333))  # подключемся к серверному сокету

        t = Thread(target=in_thread, args=(sock,), daemon=True)
        t.start()

        while True:
            message = input()
            sock.send(bytes(message, encoding='UTF-8'))

    sock.close()