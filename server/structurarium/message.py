import msgpack


class Message(object):
    
    def __init__(self, action, *args):
        self.action = action
        self.args = args

    @staticmethod
    def loads(message):
        message = msgpack.unpackb(message)
        action = message['action']
        args = message['args']
        return Message(action, *args)

    def dumps(self):
        return msgpack.packb(dict(action=self.action, args=self.args))