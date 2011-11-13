from base import Base
from util import check_if_key_exists


class List(Base):

    def __init__(self, server, key):
        super(String, self).__init__(server, key)
        self.value = []

    def __repr__(self):
        return repr(self.value)

    @staticmethod
    def LPOP(server, *keys):
        for key in keys:
            if key in server.dict:
                value = server.dict[key]
                if not value.is_dead:
                    if isinstance(value, List):
                        head = value.value[0]
                        value.value = value[1:]
                        return head

    @staticmethod
    def RPOP(server, *keys):
        for key in keys:
            if key in server.dict:
                value = server.dict[key]
                if not value.is_dead:
                    if isinstance(value, List):
                        return value.value.pop()
        return 'KEY DOES NOT EXISTS'

    @staticmethod
    def RPOPLPUSH(server, source, destination):
        if source in server.dict:
            source_value = server.dict[source]
            if not source_value.is_dead:
                if isinstance(source_value, List):
                    return 'WRONG VALUE'
                if destination in server.dict:
                    destination_value = server.dict[destination]
                    if not destination_value.is_dead:
                        if isinstance(destination_value, List):
                            return 'WRONG VALUE'
                        tail = source_value.pop()
                        destination_value.insert(0, tail)
                        return tail
                    else:
                        return 'KEY DOES NOT EXISTS'
            else:
                return 'KEY DOES NOT EXISTS'
        else:
            return 'KEY DOES NOT EXISTS'

    @staticmethod
    def LPOPRPUSH(server, source, destination):
        if source in server.dict:
            source_value = server.dict[source]
            if isinstance(source_value, List):
                return 'WRONG VALUE'
            if not source_value.is_dead:
                if destination in server.dict:
                    destination_value = server.dict[destination]
                    if not destination_value.is_dead:
                        if isinstance(destination_value, List):
                            return 'WRONG VALUE'
                        head = source_value.value.pop()
                        destination_value.value.insert(0, tail)
                        return head
        return 'KEY DOES NOT EXISTS'
    
    @check_if_key_exists
    def LINDEX(self, index):
        return self.value[index]

    @check_if_key_exists
    def LINSERT(self, index, value):
        return self.value.insert(index, value)

    @check_if_key_exists
    def LLEN(self):
        return len(self.value)

    @check_if_key_exists
    def LPOP(self):
        value = self.value[0]
        self.value = self.value[1:]
        return value        

    @check_if_key_exists
    def LRANGE(self, start, end):
        return self.value[start:end]

    @check_if_key_exists
    def LREM(self, count, value):
        nb_removed_elements = 0
        copy = self.value
        mishmached = False
        if count < 0:
            count = abs(count)
            copy = list(reversed(copy))
            mishmached = True
        elif count == 0:
            count = None
        for i in range(count):
            if value in copy:
                nb_removed_elements += 1
                copy.remove(value)
            else:
                break
        if mishmached:
            copy.reverse()
        self.value = copy
        return nb_removed_elements

    @check_if_key_exists
    def LSET(self, index, value):
        try:
            self.value[index] = value
        except IndexError:
            return 'INDEX ERROR'
        else:
            return 'OK'

    @staticmethod
    def RPUSH(server, key, *values):
        if key in server.dict:
            if not server.dict[key.is_dead:
                server.dict[key] = List(server, key)
        else:
            server.dict[key] = List(server, key)
        for value in values:
            server.dict[key].append(value)
        return len(server.dict[key])

    @staticmethod
    def RPUSHX(server, key, *values):
        if key in server.dict:
            if not server.dict[key.is_dead:
                return 'KEY DOES NOT EXISTS'
            else:
                return self.RPUSH(server, key, *values)
        else:
            return 'KEY DOES NOT EXISTS'

    @staticmethod
    def LPUSH(server, key, *values):
        if key in server.dict:
            if not server.dict[key.is_dead:
                server.dict[key] = List(server, key)
        else:
            server.dict[key] = List(server, key)
        for value in values:
            server.dict[key].insert(0,value)
        return len(server.dict[key])

    @staticmethod
    def LPUSHX(server, key, *values):
        if key in server.dict:
            if not server.dict[key.is_dead:
                return 'KEY DOES NOT EXISTS'
            else:
                return self.LPUSH(server, key, *values)
        else:
            return 'KEY DOES NOT EXISTS'
