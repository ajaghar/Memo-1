import sys, os
from types import FunctionType, MethodType
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import zmq

from message import Message
from util import import_class, handle_response
import exception


class Client(object):
    
    def __init__(self, location, port, **kwargs):
        self.options = kwargs
        self.options['location'] = location
        self.options['port'] = port
        location = 'tcp://%s:%s' % (location, port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(location)

        self.__load__()

    def __getattribute__(self, attribute):
        try:
            return super(Client, self).__getattribute__(attribute)
        except AttributeError:
            # this method is not defined by a local structure class
            # let's try to call it nonetheless
            def method(self, *args):
                message = Message(attribute, *args)
                message = self.send_and_recv(message)
                if message.action == 'RESPONSE':
                    if len(message.args) == 1:
                        return message.args[0]
                    else:
                        return message.args
                else:
                    handle_response(message)
            return MethodType(method, self, type(self))

    def __add_structure__(self, structure_class):
        structure_class.init(self)
        for action_name in dir(structure_class):
            if action_name.isupper():
                function = getattr(structure_class, action_name)
                if isinstance(function, FunctionType):
                    bound_action_method = MethodType(function, self, type(self))
                    setattr(self, action_name, bound_action_method)

    def __load__(self):
        structures_name = self.STRUCTURES()
        for structure_name in structures_name:
            structure_class_module_name = structure_name.lower()
            structure_class_name = structure_class_module_name.capitalize()
            structure_class_path = 'dominus.structure.%s.%s' % (structure_class_module_name, structure_class_name)
            structure_class = import_class(structure_class_path)
            if structure_class is not None:
                self.__add_structure__(structure_class)

    def send_and_recv(self, message):
        self.socket.send(message.dumps())
        message = Message.loads(self.socket.recv())
        return message

    def STRUCTURES(self):
        message = Message('STRUCTURES')
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args
        else:
            handle_response(message)


if __name__ == '__main__':
    client = Client('127.0.0.1', port=8000, publisher_port=8001)
    client.SUGGEST('A')
    client.SUGGESTADD('A', 'FOO', 1)
    client.SUGGESTADD('A', 'FOOBAR', 1)
    client.SUGGESTADD('A', 'FOOBAZ', 1)
    client.SUGGESTADD('A', 'FOOBARBAZ', 1)
    print client.SUGGESTSEARCH('A', 'FOO', 2)