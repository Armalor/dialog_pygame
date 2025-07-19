from socketserver import ThreadingTCPServer, BaseRequestHandler
import re
from queue import Queue
from typing import Dict, List
from time import perf_counter, sleep
from statistics import mean
from threading import Thread, Lock
from enum import IntEnum, Enum
from dataclasses import dataclass


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
                break

            data = data.decode()

            print(data)

            try:
                ...

            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", self.client_address)