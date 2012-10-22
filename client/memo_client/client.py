from types import FunctionType
from types import MethodType

from exception import MemoServerError
from util import ClientSocket


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
        sock = ClientSocket(self.address)
        response = sock.send_and_recv(message)
        if response[0] == 'RESPONSE':
            return response[1]
        else:
            raise MemoServerError(response[1])
