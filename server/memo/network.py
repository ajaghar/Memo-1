from __pypy__.thread import atomic
import socket


# FIXME: move this in main
class ServerSocket(object):
    # adapted from Python tutorial
    # http://docs.python.org/howto/sockets.html

    def __init__(self, address, port):
        # create an INET, STREAMing socket
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        # bind the socket to a public host,
        # and a well-known port
        self.sock.bind((address, port))
        # become a server socket
        self.sock.listen(5)
        # connections will be ready to be picked up by workers
        self.queue = list()

    def recv(self):
        cnx = self.sock.accept()[0]  # leave the address
        with atomic:
            self.queue.insert(0, cnx)
