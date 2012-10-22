from base import Base
from util import check_if_key_exists


class Hashes(Base):

    def __init__(self,  server, key):
        super(Hashes, self).__init__(self, server, key)
        self.dict = dict()

    @staticmethod
    def HSET(server, key, dict):
        new = False
        if key in server.dict:
            if server.dict[key].is_dead:
                server.dict[key] = Hashes(server, key)
                new = True
            else:
                if not isinstance(server.dict[key], Hashes):
                    server.dict[key] = Hashes(server, key)
                    new = True
        server.dict.update(dict)
        return True

    @check_if_key_exists
    def HDEL(self, keys):
        deleted = 0
        for key in keys:
            try:
                del self.dict[key]
            except KeyError:
                pass
            else:
                deleted += 1
        return deleted

    @check_if_key_exists
    def HEXISTS(self, key):
        return key in self.dict

    @check_if_key_exists
    def HGET(self, keys):
        values = []
        for key in keys:
            if key in self.dict:
                values.append(self.dict[key])
        return values

    @check_if_key_exists
    def HGETALL(self):
        return self.dict

    @check_if_key_exists
    def HINCRBY(self, field, increment):
        if not istance(self.dict[field], int):
            self.dict[field] = 0
        self.dict[field] += increment
        return self.dict[field]

    @check_if_key_exists
    def HKEYS(self):
        return self.dict.keys()

    @check_if_key_exists
    def HLEN(self):
        return len(self.dict)

    @staticmethod
    def HSETNX(server, key, field, value):
        if key in server.dict:
            if server.dict[key].is_dead:
                server.dict[key] = Hashes(server, key)
        if not key in server.dict[key].dict:
            server.dict[key].dict[field] = value
            return True
        return False

    @check_if_key_exists
    def HVALS(self):
        return self.dict.values()