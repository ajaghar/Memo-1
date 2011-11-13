from base import Base

from util import check_if_key_exists


class String(Base):

    def __init__(self, server, key, value):
        super(String, self).__init__(server, key)
        self.value = value

    def __repr__(self):
        return repr(self.value)

    @staticmethod
    def SETSTRING(server, key, value):
        server.dict[key] = String(server, key, value)
        return 'OK'

    @staticmethod
    def SETSTRINGEX(server, key, seconds, value):
        String.SETSTRING(server, key, value)
        value = self.server.dict[key]
        value.ttl = seconds
        return 'OK'

    @staticmethod
    def SETSTRINGNX(server, key, value):
        if key in server.dict:
            return 'KEY DOES EXISTS'
        return String.SETSTRING(server, key, value)

    @check_if_key_exists
    def APPEND(self, value):
        self.value += value
        return len(self.value)

    @check_if_key_exists
    def GET(self):
        return self.value

    @check_if_key_exists 
    def GETRANGE(self, start, end):
        return self.value[start:end]

    @check_if_key_exists
    def GETSET(self, value):
        old = self.value
        self.value = value
        return old

    @check_if_key_exists
    def SETRANGE(self, offset, value):
        old = self.value[offset:]
        self.value = old + value
        return 'OK'
