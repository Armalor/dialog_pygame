import socket
from net import Net

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
sock.bind(('', Net.SERVER_PORT))  # связываем сокет с портом, где он будет ожидать сообщения
sock.listen(10)  # указываем сколько может сокет принимать соединений
print('Server is running, please, press ctrl+c to stop')
while True:
    conn, addr = sock.accept()  # начинаем принимать соединения
    print('connected:', addr)  # выводим информацию о подключении
    data = conn.recv(1024)  # принимаем данные от клиента, по 1024 байт
    print(str(data))
    conn.send(b'Answer: ' + data.upper())  # в ответ клиенту отправляем сообщение в верхнем регистре

conn.close()  # закрываем соединение
