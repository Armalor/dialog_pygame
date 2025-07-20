from socketserver import ThreadingTCPServer, BaseRequestHandler


class ConnectionHandler(BaseRequestHandler):

    def __init__(self, request, client_address, server):

        self.users = dict()

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
                print(f"Client unexpectedly closed connection")
                break

            data = data.decode()

            print(data)

            if self.client_address not in self.users:
                answer = ''
            elif self.users[self.client_address] is None:
                self.users[self.client_address] = data

            try:
                self.request.sendall(b'test: }' + data)

            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", self.client_address)