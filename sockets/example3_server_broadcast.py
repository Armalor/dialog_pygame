import socket
import threading

from net import Net

HOST = ''
PORT = Net.SERVER_PORT

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

clients = []

client_names = dict()


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    clients.append(client_socket)
    client_names[client_socket] = client_address[0]
    try:
        while True:
            message: str = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {client_address}: {message}")
            if message.startswith('/name'):
                client_names[client_socket] = message[6:]

            broadcast(message, client_socket)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        clients.remove(client_socket)
        client_socket.close()
        print(f"Connection from {client_address} closed")


def broadcast(message, source_socket):
    for client in clients:
        if client != source_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                clients.remove(client)
                client.close()


def server():
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        thread.start()


if __name__ == "__main__":
    server()
