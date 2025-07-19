from tkinter import *
from tkinter import ttk
from socketserver import ThreadingTCPServer
from threading import Thread
from time import sleep, perf_counter
from typing import Dict, List


from connection_handler import ConnectionHandler
from net import Net


HOST = ""
PORT = Net.SERVER_PORT


def serve(server):
    with server:
        print('Start server')
        server.serve_forever(poll_interval=0.05)


if __name__ == "__main__":
    server = ThreadingTCPServer((HOST, PORT), ConnectionHandler)
    with server:
        print('Start server')
        server.serve_forever(poll_interval=0.05)
