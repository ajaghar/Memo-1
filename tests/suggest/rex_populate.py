from rex.rex import Rex


rex = Rex('127.0.0.1', port=8000)

rex.SUGGESTADD('SPELLCHECKER')

words = open('wordlist.txt')
for word in words:
    rex.SUGGESTADD('SPELLCHECKER', word.strip())

words.close()
