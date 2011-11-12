import sys, os
from types import FunctionType, MethodType
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

import zmq

from message import Message
from util import import_class
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
            print structure_class_path
            structure_class = import_class(structure_class_path)
            self.__add_structure__(structure_class)

    def send_and_recv(self, message):
        self.socket.send(message.dumps())
        message = Message.loads(self.socket.recv())
        return message

    def DEL(self, *args):
        message = Message('DEL', *args)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            pass
        else:
            handle_response(message)

    def EXISTS(self, key):
        message = Message('EXISTS', key)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)

    def EXPIRE(self, key, seconds):
        message = Message('EXPIRE', key, seconds)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)

    def EXPIREAT(self, key, timestamp):
        message = Message('EXPIREAT', key, timestamp)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return
        else:
            handle_response(message)

    def KEYS(self, pattern=None):
        pattern = '' if pattern is None else pattern
        message = Message('KEYS', pattern)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args
        else:
            handle_response(message)

    def PERSIST(self, key):
        message = Message('PERSIST', key)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            pass
        else:
            handle_response(message)

    def RANDOMKEY(self):
        message = Message('RANDOMEKEY')
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)

    def RENAME(self, key, newkey):
        message = Message('RENAME', key, newkey)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            pass
        else:
            handle_response(message)

    def RENAMENX(self, key, newkey):
        message = Message('RENAMENX', key, newkey)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            pass
        else:
            handle_response(message)

    def STRUCTURES(self):
        message = Message('STRUCTURES')
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)

    def TTL(self, key):
        message = Message('TTL', key)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)

    def STRUCTURE(self, key):
        message = Message('STRUCTURE', key)
        message = self.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)


if __name__ == '__main__':
    client = Client('127.0.0.1', port=8000, publisher_port=8001)
    client.SETSTRING('FOO', 'BARBAZ')
    print client.GET('FOO')