from socketserver import ThreadingTCPServer, BaseRequestHandler


class ConnectionHandler(BaseRequestHandler):

    def __init__(self, request, client_address, server):

        super().__init__(request, client_address, server)

    def handle(self):
        print("Connected by", self.client_address)
        while True:
            try:
                data = self.request.recv(1024)
            except ConnectionError:
                print(f"Client suddenly closed while receiving")
                break
            if not data:
                print(f"Client suddenly closed while receiving")

            data = data.decode()

            print(data)

            try:
                ...

            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", self.client_address)


def serve(server):
    with server:
        print('Start server')
        server.serve_forever(poll_interval=0.05)


if __name__ == "__main__":
    HOST = ""
    PORT = 11_111

    server = ThreadingTCPServer((HOST, PORT), ConnectionHandler)
    serve(server)