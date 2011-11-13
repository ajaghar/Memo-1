from time import time

from util import check_if_key_exists


class Base(object):
    
    def __init__(self, server, key):
        self.server = server
        self.key = key
        self.expiration_time = None
        self.started_at = None

    @classmethod
    def structure_name(cls):
        return cls.__name__.upper()
        
    @classmethod
    def init(cls, server):
        server._structures.append(cls.structure_name())

    def expire_at(self, timestamp):
        self.expiration_time = timestamp
        self.started_at = time()

    def set_ttl(self, ttl):
        self.started_at = time()
        self.expiration_time = self.started_at + ttl

    def get_ttl(self):
        if not self.is_dead:
            return self.expiration_time - time()
        else:
            return None
    
    ttl = property(get_ttl, set_ttl)

    def persist(self):
        self.expiration_time = None

    @property
    def is_dead(self):
        if self.expiration_time is not None and time() > self.expiration_time:
            del self.server.dict[self.key]
            return True
        return False

    @check_if_key_exists
    def STRUCTURE(self):
        return self.structure_name()

    @check_if_key_exists
    def TTL(self):
        return self.ttl
