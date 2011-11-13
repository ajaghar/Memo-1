import zmq

from message import Message
from structurarium import Structurarium


class Dominus(object):

    def __init__(self, location):
        self.location = location
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.location)


    def load(self, structure_class):
        methods = [e for e in dir(structure_class) if e.isupper()]
        

    def send(self, message):
        return Message.load(self.socket.send(message))