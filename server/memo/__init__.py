import thread

from structures.suggest import Suggest
from network import ServerSocket
from worker import Worker
from memo import Memo

WORKERS = 5


def main():
    server = ServerSocket('127.0.0.1', 9500)
    memo = Memo()
    memo.add_structure(Suggest)

    for i in range(WORKERS):
        worker = Worker(memo, server)
        thread.start_new_thread(worker.start, ())
    while True:
        server.recv()
