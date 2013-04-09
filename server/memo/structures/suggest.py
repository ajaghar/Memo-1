from base import Base
from util import write
from util import with_atomic
from util import check_if_key_exists


def iter_trigrams(string):
    for start in range(len(string))[:-2]:
        trigram = string[start:start+3]
        yield trigram


class Suggest(Base):

    def __init__(self, server, key):
        super(Suggest, self).__init__(server, key)
        self.trigrams = dict()

    @staticmethod
    @write
    @with_atomic
    def SUGGESTADD(server, key, *strings):
        if key in server.dict:
            if server.dict[key].is_dead:
                server.dict[key] = Suggest(server, key)
            else:
                if not isinstance(server.dict[key], Suggest):
                    return 'WRONG VALUE'
        else:
            server.dict[key] = Suggest(server, key)
        value = server.dict[key]
        for string in strings:
            if len(string) < 3:
                continue
            else:

                for trigram in iter_trigrams(string):
                    if not trigram in value.trigrams:
                        value.trigrams[trigram] = list()
                    value.trigrams[trigram].append(string)
        return 'OK'

    @check_if_key_exists
    @with_atomic
    def SUGGEST(self, string, limit=10):
        suggestions = dict()
        for trigram in iter_trigrams(string):
            strings = self.trigrams.get(trigram, [])
            for s in strings:
                try:
                    suggestions[s] += 1
                except:
                    suggestions[s] = 1
        suggestions = sorted(
            suggestions.keys(),
            key=lambda x: suggestions[x],
            reverse=True
        )
        suggestions = suggestions[:10]
        return suggestions
