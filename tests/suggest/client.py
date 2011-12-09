import json

from rex.rex import Rex


rex = Rex('127.0.0.1', port=8000)

rex.SUGGESTADD('SPELLCHECKER')

words = open('wordlist.txt')
for word in words:
    rex.SUGGESTADD('SPELLCHECKER', word.strip())

words.close()


missplellings_w_corrections_file = open('missplellings_w_corrections.txt')
missplellings_w_corrections = missplellings_w_corrections_file.read()
missplellings_w_corrections_file.close()
missplellings_w_corrections = json.loads(missplellings_w_corrections)


hit = 0
total = len(missplellings_w_corrections)

for mistake, corrections in missplellings_w_corrections.iteritems():
    suggestions = rex.SUGGEST('SPELLCHECKER', mistake)
    for correction in corrections:
        if correction in suggestions:
            # at the end ``miss`` can be superior to total
            # because we want all possible correction
            # to be suggested :)
            hit += 1

print hit, '/', total
