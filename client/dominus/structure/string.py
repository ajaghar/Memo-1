from base import Base
from dominus.util import handle_response
from dominus.message import Message


class String(Base):

    @classmethod
    def init(cls, client):
        super(String, cls).init(client)

    @staticmethod
    def SETSTRING(client, key, value):
        message = Message('SETSTRING', key, value).dumps()
        client.socket.send(message)
        message = client.socket.recv()
        message = Message.loads(message)
        if message.action == 'RESPONSE':
            if message.args[0] == 'OK':
                return True
        handle_response(message)

    @staticmethod
    def SETSTRINGNX(client, key, value):
        message = Message('SETSTRINGNX', key, value)
        if message.response = 'RESPONSE':
            if message.response.args[0] == 'OK':
                return True
        handle_response(message)

    @staticmethod
    def APPEND(client, key, value):
        message = Message('APPEND', key, value)
        if message.response = 'RESPONSE':
            return message.response.args[0]
        else:
            handle_response(message)

    @staticmethod
    def GETRANGE(self, start, end):
        message = Message('GETRANGE', start, end)
        if message.response = 'RESPONSE':
            return message.response.args[0]
        else:
            handle_response(message)

    @staticmethod
    def GETSET(client, key, value):
        message = Message('GETSET', key, value)
        if message.response = 'RESPONSE':
            return message.response.args[0]
        else:
            handle_response(message)

    @staticmethod
    def SETRANGE(self, offset, value):
        message = Message('SETRANGE', offset, value)
        if message.response = 'RESPONSE':
            if message.response.args[0] == 'OK':
                return True
        handle_response(message)

    @staticmethod
    def STRLEN(self, key):
        message = Message('STRLEN', key)
        if message.response = 'RESPONSE':
            return message.args[0]
        handle_response(message)
