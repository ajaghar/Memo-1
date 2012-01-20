from structurarium.routines import loop, Return

import zmq
from zmq import *

from zmq.core.context import Context as OriginalContext
from zmq.core.socket import Socket as OriginalSocket

from structurarium.routines import loop, reschedule

class _Context(OriginalContext):

    def socket(self, socket_type):
        if self.closed:
            raise ZMQError(ENOTSUP)
        return _Socket(self, socket_type)


class _Socket(OriginalSocket):

    def __init__(self, context, socket_type):
        loop.register(self.getsockopt(FD))

    def _wait(self, event):
        while True:
            fileno = self.getsockopt(FD)
            yield loop.wait_fileno(fileno)
            events = self.getsockopt(zmq.EVENTS)
            if events & event:
                yield Return()
            else:
                yield reschedule

    def send(self, data, flags=0, copy=True, track=False):
        # if we're given the NOBLOCK flag act as normal and let the EAGAIN get raised
        if flags & zmq.NOBLOCK:
            yield Return(super(_Socket, self).send(data, flags, copy, track))
        # ensure the zmq.NOBLOCK flag is part of flags
        flags |= zmq.NOBLOCK
        while True: # Attempt to complete this operation indefinitely, blocking the current greenlet
            try:
                # attempt the actual call
                yield Return(super(_Socket, self).send(data, flags, copy, track))
            except zmq.ZMQError, e:
                # if the raised ZMQError is not EAGAIN, reraise
                if e.errno != zmq.EAGAIN:
                    raise
            # defer to the event loop until we're notified the socket is writable
            yield self._wait(zmq.POLLOUT)

    def recv(self, flags=0, copy=True, track=False):
        if flags & zmq.NOBLOCK:
            yield Return(super(_Socket, self).recv(flags, copy, track))
        flags |= zmq.NOBLOCK
        while True:
            try:
                yield Return(super(_Socket, self).recv(flags, copy, track))
            except zmq.ZMQError, e:
                if e.errno != zmq.EAGAIN:
                    raise
            yield self._wait(zmq.POLLIN)

    def recv_multipart(self, flags=0, copy=True, track=False):
        while self.getsockopt(ZMQ_RCVMORE):
            part = yield self.recv(flags, copy=copy, track=track)
            parts.append(part)

        yield Return(parts)

    def send_multipart(
            self,
            msg_parts,
            flags=0,
            copy=True,
            track=False,
            prefix=None
        ):
        if prefix:
            if isinstance(prefix, bytes):
                prefix = [prefix]
            for msg in prefix:
                yield self.send(msg, SNDMORE|flags)
        for msg in msg_parts[:-1]:
            yield self.send(msg, SNDMORE|flags, copy=copy, track=track)
        # Send the last part without the extra SNDMORE flag.
        r = yield self.send(msg_parts[-1], flags, copy=copy, track=track)
        yield Return(r)
