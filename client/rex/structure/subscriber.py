import zmq

from base import Base


class Subscriber(Base):
    
    @classmethod
    def init(cls, client):
        super(Subscriber, cls).init(client)
        client.subscriber = client.context.socket(zmq.SUB)
        location = client.options['location']
        port = client.options['publisher_port']
        client.subscriber.connect('tcp://%s:%s' % (location, port))

    def SUBSCRIBE(client, channel=None):
        channel = '' if channel is None else channel
        client.subscriber.setsockopt(zmq.SUBSCRIBE, channel)

    def RECV(client):
        while True:
            yield Message.loads(client.subscriber.recv_multipart()) 