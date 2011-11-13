from base import Base
from util import check_if_key_exists


class Set(Base):

    def __init__(self, server, key):
        super(Set, self).__init__(server, key)
        self.set = set()

    @staticmethod:
    def SADD(server, key, *members):
        if key in server.dict:
            value = server.dict[key]
            if not value.is_dead:
                if not isinstance(value, Set):
                    return 'WRONG VALUE'
            else:
                server.dict[key] = Set(server, key)
        else:
            server.dict[key] = Set(server, key)
        server.dict[key] = Set(server, key)
        l = len(server.dict[key])
        for member in members:
            server.dict[key].add(member)
        return len(server.dict[key]) - l
                    
    @check_if_key_exists
    def SCARD(self):
        return len(self.set)

    @check_if_key_exists
    def SDIFF(self, *keys):
        r = self.set
        for key in keys:
            s = self.server.dict[key]
            if not s.is_dead:
                if isinstance(s, Set):
                    r = r.difference(s.set)
        return r

    @check_if_key_exists
    def SDIFFSTORE(self, destination, *keys):
        r = self.SDIFF(keys)
        self.server.dict[destination] = r
        return len(r)

    @check_if_key_exists
    def SINTER(self, *keys):
        r = self.set
        for key in keys:
            s = self.server.dict[key]
            if not s.is_dead:
                if isinstance(s, Set):
                    r = r.intersection(s.set)
        return r

    @check_if_key_exists
    def SINTERSTORE(self, destination, *keys):
        r = self.SINTER(keys)
        self.server.dict[destination] = r
        return len(r)

    @check_if_key_exists
    def SUNION(self, *keys):
        r = self.set
        for key in keys:
            s = self.server.dict[key]
            if not s.is_dead:
                if isinstance(s, Set):
                    r = r.union(s.set)
        return r

    @check_if_key_exists
    def SUNIONSTORE(self, destination, *keys):
        r = self.SUNION(keys)
        self.server.dict[destination] = r
        return len(r)
    
    @check_if_key_exists
    def SISMEMBER(self, *members):
        for member in members:
            if not member in self.set:
                return False
        return True

    @check_if_key_exists
    def SMEMEBERS(self):
        return list(self.set)

    @check_if_key_exists
    def MOVE(self, destination, member):
        if member in self.set:
            if destination in self.server.dict:
                value = self.server.dict[destination]
                if not value.is_dead:
                    if isinstance(value, Set):
                        self.set.remove(member)
                        value.add(member)
                        return True
                    return 'WRONG VALUE'
                return 'KEY DOES NOT EXISTS'
            return 'KEY DOES NOT EXISTS'
        else:
            return False

    @check_if_key_exists
    def SPOP(self):
        try:
            return self.set.pop()
        except KeyError:
            return None

    @check_if_key_exists
    def SRANDMEMBER(self):
        member = self.SPOP()
        if member is not None:
            self.set.add(member)
        return member

    @check_if_key_exists
    def SREM(self, *members):
        removed = 0
        for member in members:
            if member in self.set:
                self.set.remove(member)
                removed += 1
        return removed

    