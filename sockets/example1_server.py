import socket

HOST = ""  # Использовать все адреса: виден и снаружи, и изнутри
PORT = 11_111  # Произвольный незарезервированный порт


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(10)

        while True:
            print("Waiting for connection...")
            sock, addr = serv_sock.accept()
            with sock:
                print("Connected by", addr)
                while True:
                    # Receive
                    try:
                        data = sock.recv(1024)
                    except ConnectionError:
                        print(f"Client suddenly closed while receiving")
                        break
                    if not data:
                        print(f"Client unexpectedly closed connection")
                        break

                    print(f"Received: {data} from: {addr}")
                    data = data.upper()
                    # Send
                    print(f"Send: {data} to: {addr}")
                    try:
                        sock.sendall(data)
                    except ConnectionError:
                        print(f"Client suddenly closed, cannot send")
                        break
            print("Disconnected by", addr)