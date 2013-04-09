from memo_client import MemoClient


memo = MemoClient('127.0.0.1', 9500)
memo.SUGGESTADD('foobar', 'flubur', 'blublu')
print memo.SUGGEST('foo')
