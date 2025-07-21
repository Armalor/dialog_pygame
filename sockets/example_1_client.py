import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет

from net import Net

client = Net.get_local_ip()
print(f'local IP: {client}')
host = Net.scan()
if host:
    print(f'server host: {host}')
    sock.connect((host, Net.SERVER_PORT))  # подключемся к серверному сокету

    while True:
        message = input()
        sock.send(bytes(message, encoding='UTF-8'))  # отправляем сообщение
        data = sock.recv(1024)  # читаем ответ от серверного сокета
        print(data.decode())
    sock.close()  # закрываем соединение
