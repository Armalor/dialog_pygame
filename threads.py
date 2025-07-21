from threading import Thread, Lock
from time import sleep
import random

counter = 0

blocker = Lock()


def in_thread(stop=1000_000, name=None):
    global counter
    for i in range(stop):
        # sleep(random.random())
        with blocker:
            counter += 1

        # print(f'thread {name}: {counter}')


if __name__ == '__main__':
    # in_thread(10, 'main')

    print(f'Counter: {counter}')

    threads = []
    for i in range(5):
        t = Thread(target=in_thread, args=(1_000_000, f'thread_{i}'))
        t.start()

    for t in threads:
        t.join()

    print(f'Counter after: {counter}')