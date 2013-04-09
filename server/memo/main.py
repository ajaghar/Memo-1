#!/usr/bin/env python
from thread import start_new_thread

from structures.suggest import Suggest
from network import ServerSocket
from worker import Worker
from memo import Memo

WORKERS = 5


def main():
    server = ServerSocket('127.0.0.1', 9512)
    memo = Memo()
    memo.add_structure(Suggest)
    workers = list()
    for i in range(WORKERS):
        worker = Worker(memo, server)
        workers.append(worker)
        start_new_thread(worker.start, ())
    while True:
        try:
            server.recv()
        except KeyboardInterrupt:
            server.close()
            for worker in workers:
                worker.running = False

if __name__ == '__main__':
    main()
