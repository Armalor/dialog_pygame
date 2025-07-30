from threading import Thread, Lock
from time import sleep
import random

counter = 0

blocker = Lock()


def in_thread(stop, lock: Lock = Lock(), name=None):
    global counter
    for i in range(stop):
        with lock:
            temp = counter
            sleep(0.0001)
            counter = temp + 1

    print(f'thread {name}: {counter}')


if __name__ == '__main__':
    # in_thread(10, 'main')

    print(f'Counter: {counter}')

    threads = []
    for i in range(10):
        t = Thread(target=in_thread, args=(10, blocker, f'thread_{i}'), daemon=True)
        t.start()

        threads.append(t)
    #
    # for t in threads:
    #     t.join()

    print(f'Counter after: {counter}')
