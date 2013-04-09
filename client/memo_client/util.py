import socket
import struct
import cPickle


class ClientSocket:
    # adapted from http://docs.python.org/howto/sockets.html

    BUFSIZE = 1024
    LONGSIZE = 8

    def __init__(self, address):
        self.address = address
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def send_and_recv(self, msg):
        self.sock.connect(self.address)
        # prepare and send msg
        msg = cPickle.dumps(msg)
        msg = struct.pack('L', len(msg)) + msg
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError('socket connection broken')
            totalsent += sent
        # recv message
        msg = ''
        size = None
        while True:
            msg += self.sock.recv(self.BUFSIZE)
            if len(msg) and (not size) and len(msg) >= self.LONGSIZE:
                size = struct.unpack('L', msg[:self.LONGSIZE])[0]
                msg = msg[self.LONGSIZE:]
            if size and len(msg) == size:
                self.sock.close()
                return cPickle.loads(msg)
