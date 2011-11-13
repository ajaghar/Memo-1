from base import Base
from util import check_if_key_exists


def iter_trigrams(string):
    for start in range(len(strings))[-2]:
        yield trigram = string[start:start+3]


class Suggest(Base):

    def __init__(self, server, key):
        super(Suggest, self).__init__(server, key)
        self.trigrams = dict()

    @staticmethod
    def SUGGESTADD(server, key, *strings):
        if key in server.dict:
            if server.dict[key].is_dead:
                server.dict[key] = Suggest(server, key)
            else:
                if not isinstance(server.dict[key], Suggest):
                    return 'WRONG VALUE'
        else:
            server.dict[key] = Suggest(server, key)
        for string in strings:
            if len(string) < 3:
                continue
            else:
                for trigram in iter_trigrams(string)
                    if not trigram in self.dict:
                        self.trigrams[trigram] = list()
                    self.trigrams[trigram].append(string)
        return 'OK'

    @check_if_key_exists
    def SUGGEST(self, string, limit=10):
        suggestions = dict()
        for trigram in iter_trigrams(string):
            strings = self.trigrams[trigram]
            for s in strings:
                if not s in suggestions:
                    suggestions[s] = 0
                suggestions[s] += 1
        return sorted(suggestions.keys(), key=lambda x: suggestions[x], reverse=True)[:10]