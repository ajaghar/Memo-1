from __pypy__.thread import atomic
import struct
import cPickle


BUFSIZE = 1024
LONGSIZE = 8


def recv(cnx):
    msg = ''
    size = None
    while True:
        msg = msg + cnx.recv(BUFSIZE)
        if len(msg) and (not size) and (len(msg) >= LONGSIZE):
            size = struct.unpack('L', msg[:LONGSIZE])[0]
            msg = msg[LONGSIZE:]
        if size and len(msg) == size:
            return cPickle.loads(msg)


def send(cnx, msg):
    msg = cPickle.dumps(msg)
    msg = struct.pack('L', len(msg)) + msg
    totalsent = 0
    while totalsent < len(msg):
        sent = cnx.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError('socket connection broken')
        totalsent = totalsent + sent
    cnx.close()


class Worker(object):

    def __init__(self, memo, server):
        self.memo = memo
        self.running = True
        self.server = server

    def start(self):
        cnx = None
        while self.running:
            with atomic:
                if self.server.queue:
                    cnx = self.server.queue.pop()
            if cnx:
                command = recv(cnx)
                send(cnx, self.memo.play(command))
