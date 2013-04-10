#!/usr/bin/env python
import signal
from thread import start_new_thread

from structures.suggest import Suggest
from network import ServerSocket
from worker import Worker
from memo import Memo

WORKERS = 2


def main():
    server = ServerSocket('127.0.0.1', 9517)
    memo = Memo()
    memo.add_structure(Suggest)
    workers = list()
    for i in range(WORKERS):
        worker = Worker(memo, server)
        workers.append(worker)
        start_new_thread(worker.start, ())

    running = True

    def close():
        global running
        running = False
        server.close()
        for worker in workers:
            worker.running = False

    signal.signal(signal.SIGINT, close)

    while running:
        server.recv()

if __name__ == '__main__':
    main()
