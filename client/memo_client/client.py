from types import FunctionType
from types import MethodType
from multiprocessing.connection import Client


from exception import MemoServerError


class MemoClient(object):

    def __init__(self, location, port):
        self.address = (location, port)

    def __getattribute__(self, attribute):
        try:
            return super(MemoClient, self).__getattribute__(attribute)
        except AttributeError:
            def method(self, *args):
                message = (attribute, args)
                response = self.send_and_recv(message)
                return response
            return MethodType(method, self, type(self))

    def __add_structure__(self, structure_class):
        structure_class.init(self)
        for action_name in dir(structure_class):
            if action_name.isupper():
                function = getattr(structure_class, action_name)
                if isinstance(function, FunctionType):
                    bound_action_method = MethodType(function, self, type(self))
                    setattr(self, action_name, bound_action_method)


    def send_and_recv(self, message):
        connection = Client(self.address, family='AF_INET')
        connection.send(message)
        response = connection.recv()
        connection.close()
        if response[0] == 'RESPONSE':
            return response[1]
        else:
            raise MemoServerError(response[1])


if __name__ == '__main__':
    client = Memo('127.0.0.1', port=8000, publisher_port=8001)
    client.SUGGEST('A')
    client.SUGGESTADD('A', 'FOO', 1)
    client.SUGGESTADD('A', 'FOOBAR', 1)
    client.SUGGESTADD('A', 'FOOBAZ', 1)
    client.SUGGESTADD('A', 'FOOBARBAZ', 1)
    print client.SUGGESTSEARCH('A', 'FOO', 2)
