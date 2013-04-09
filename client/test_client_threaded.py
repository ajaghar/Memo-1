from __pypy__.thread import atomic
from thread import start_new_thread

from memo_client import MemoClient


memo = MemoClient('127.0.0.1', 9511)  # thread safe
mistakes = list()

print 'start training'
with open('mistakes.txt') as r:
    for line in r:
        line = line.strip()
        mistake, word = line.split('->')
        mistakes.append((mistake, word))
        memo.SUGGESTADD('search', word)

print 'training done'
count = 0
total = len(mistakes)
running = 0

def suggest():
    global count, mistakes, running
    running += 1
    while True:
        with atomic:
            if mistakes:
                mistake, word = mistakes.pop()
            else:
                running -= 1
                return
        suggest = memo.SUGGEST('search', mistake)
        if suggest:
            if suggest[0] == word:
                count += 1


print 'start spellchecking'
for x in range(5):
    start_new_thread(suggest, ())

while running:
    pass

print count, 'out of', total
