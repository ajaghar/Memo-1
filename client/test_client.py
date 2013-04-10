from memo_client import MemoClient


memo = MemoClient('127.0.0.1', 9517)  # thread safe
mistakes = dict()

print 'start training'
with open('mistakes.txt') as r:
    for line in r:
        line = line.strip()
        mistake, word = line.split('->')
        mistakes[mistake] = word
        memo.SUGGESTADD('search', word)

print 'training done'
corrections = 0


print 'start spellchecking'
for mistake, word in mistakes.iteritems():
    suggest = memo.SUGGEST('search', mistake)
    if suggest:
        if suggest[0] == word:
            corrections += 1
print corrections, 'out of', len(mistakes)
