class Base(object):
    
    @classmethod
    def init(cls, client):
        cls.client = client

    @staticmethod
    def GET(client, key):
        message = Message('GET', key).dumps()
        message = client.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args[0]
        else:
            handle_response(message)
    
    @staticmethod
    def MGET(client, *keys)
        message = Message('MGET', *keys).dumps()
        message = client.send_and_recv(message)
        if message.action == 'RESPONSE':
            return message.args
        else:
            handle_response(message)
    
    @staticmethod
    def MSET(client, dictionary):
        message = Message('MSET', dictionary).dumps()
        message = client.send_and_recv(message)
        if message.action == 'RESPONSE':
            if message.args[0] == 'OK':
                return True
        handle_response(message)
        
    @staticmethod
    def MSETNX(client, dictionary):
        message = Message('MSETNX', dictionary).dumps()
        message = client.send_and_recv(message)
        if message.action == 'RESPONSE':
            pass
        else:
            handle_response(message)

    @staticmethod
    def SETEX(client, key, seconds, value):
        message = Message('SETEX', key, seconds, value).dumps()
        message = client.send_and_recv(message)
        if message.action == 'RESPONSE':
            if message.args[0] == 'OK':
                return True
        else:
            handle_response(message)

    @staticmethod
    def SETNX(client, key, value):
        message = Message('SETNX', key, value).dumps()
        message = client.send_and_recv(message)
        if message.action == 'RESPONSE':
            if message.args[0] == 'OK':
                return True
        else:
            handle_response(message)
