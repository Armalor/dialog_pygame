from socketserver import ThreadingTCPServer

from connection_handler import ConnectionHandler
from net import Net


if __name__ == "__main__":

    server = ThreadingTCPServer(("", Net.SERVER_PORT), ConnectionHandler)
    print('Start server...')
    server.serve_forever(poll_interval=0.05)
