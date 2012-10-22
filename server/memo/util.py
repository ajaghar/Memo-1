import socket
import struct
import cPickle


def check_if_key_exists(function):
    def wrapper(*args):
        self = args[0]
        key = args[1]
        if key in self.dict:
            value = self.dict[key]
            if not value.is_dead:
                return function(*args)
        return 'KEY DOES NOT EXISTS'
    return wrapper


class ServerSocket(object):
    # adapted from Python tutorial
    # http://docs.python.org/howto/sockets.html

    BUFSIZE = 1024
    LONGSIZE = 8

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

    def recv(self):
        (self.client, address) = self.sock.accept()
        msg = ''
        size = None
        while True:
            msg = msg + self.client.recv(self.BUFSIZE)
            if len(msg) and (not size) and (len(msg) >= self.LONGSIZE):
                size = struct.unpack('L', msg[:self.LONGSIZE])[0]
                msg = msg[self.LONGSIZE:]
            if size and len(msg) == size:
                return cPickle.loads(msg)

    def send(self, msg):
        msg = cPickle.dumps(msg)
        msg = struct.pack('L', len(msg)) + msg
        totalsent = 0
        while totalsent < len(msg):
            sent = self.client.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError('socket connection broken')
            totalsent = totalsent + sent
        self.client.close()
