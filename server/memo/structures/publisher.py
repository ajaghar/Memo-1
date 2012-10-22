import zmq

from base import Base

from structurarium.message import Message
from util import check_if_key_exists


class Publisher(Base):

    @classmethod
    def init(cls, server, port):
        super(Publisher, cls).init(server)
        server.publisher = server.context.socket(zmq.PUB)
        server.publisher.bind('tcp://*:%s' % port)
        print 'Publisher running on 127.0.0.1:%s' % port

    def PUBLISH(self, channel, message):
        self.bserver.publisher.send_multipart([channel, message])
        return 'OK'